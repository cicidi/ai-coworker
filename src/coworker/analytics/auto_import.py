"""Auto-import daemon: scan sessions, import new data, handle incremental updates."""
import json
import sqlite3
import time
from pathlib import Path
from datetime import datetime
from src.coworker.analytics.db import get_db
from src.coworker.analytics.import_data import import_session

HOME = Path.home()
BASE = HOME / ".coworker" / "analytics"
SESSIONS = BASE / "sessions"
OPCODE_DB = HOME / ".local" / "share" / "opencode" / "opencode.db"
POLL_INTERVAL = 1800  # 30 minutes


def get_last_imported_session(conn) -> str | None:
    """Get the most recent session in analytics DB."""
    row = conn.execute(
        "SELECT id FROM sessions ORDER BY created_at DESC LIMIT 1"
    ).fetchone()
    return row["id"] if row else None


def collect_new_claude_sessions(conn) -> list[Path]:
    """Find Claude Code sessions newer than what's in the DB."""
    if not SESSIONS.exists():
        return []
    last = get_last_imported_session(conn)
    existing = set(
        r[0] for r in conn.execute("SELECT id FROM sessions").fetchall()
    )
    # Return ALL session dirs — import_session handles incremental inserts
    # But skip ones we've already fully imported (where session.yaml hasn't changed)
    return [
        d for d in sorted(SESSIONS.iterdir())
        if d.is_dir() and not d.name.startswith('.') and (d / "session.yaml").exists()
    ]


def collect_new_opencode_sessions(conn) -> list[dict]:
    """Find OpenCode sessions not yet in analytics DB."""
    if not OPCODE_DB.exists():
        return []
    existing = set(
        r[0] for r in conn.execute("SELECT id FROM sessions WHERE ide='opencode'").fetchall()
    )
    try:
        oc = sqlite3.connect(str(OPCODE_DB))
        oc.row_factory = sqlite3.Row
        rows = oc.execute(
            "SELECT id, title, model, cost, tokens_input, tokens_output, time_created "
            "FROM session WHERE title IS NOT NULL AND title != '' "
            "ORDER BY time_created DESC"
        ).fetchall()
        oc.close()
        return [dict(r) for r in rows if r["id"] not in existing]
    except sqlite3.Error:
        return []


def import_opencode_session(session: dict, conn):
    """Import a single OpenCode session into analytics DB."""
    sid = session["id"]
    created = session.get("time_created", "")
    if created:
        try:
            created = datetime.fromtimestamp(int(created) / 1000).isoformat()
        except (ValueError, TypeError, OSError):
            pass

    conn.execute(
        """INSERT OR REPLACE INTO sessions (id, ide, model, created_at, closed_at)
           VALUES (?, 'opencode', ?, ?, ?)""",
        (sid, session.get("model", ""), created, created),
    )

    opcode = sqlite3.connect(str(OPCODE_DB))
    opcode.row_factory = sqlite3.Row
    parts = opcode.execute(
        "SELECT data, time_created FROM part WHERE session_id=? AND data IS NOT NULL ORDER BY time_created ASC",
        (sid,)
    ).fetchall()
    opcode.close()

    for seq, (data_raw, ts) in enumerate(parts):
        try:
            obj = json.loads(data_raw)
            mtype = obj.get("type", "")
            text = obj.get("text", "")
            if mtype in ("text", "reasoning") and text:
                conn.execute(
                    "INSERT OR IGNORE INTO messages (session_id, seq, type, content, ts) VALUES (?, ?, ?, ?, ?)",
                    (sid, seq, mtype, text[:8000], str(ts)),
                )
            elif mtype == "tool":
                tool_name = obj.get("name", obj.get("tool", ""))
                tool_input = json.dumps(obj.get("input", {}))[:4000]
                call_id = f"oc-{sid}-{seq}"
                conn.execute(
                    "INSERT OR IGNORE INTO tool_calls (session_id, call_id, tool, tool_type, args, seq_before, ts) VALUES (?, ?, ?, 'opencode', ?, ?, ?)",
                    (sid, call_id, tool_name, tool_input, seq, str(ts)),
                )
                if tool_name == "Skill":
                    skill_name = obj.get("input", {}).get("name", "")
                    if skill_name:
                        conn.execute("INSERT OR IGNORE INTO skills (name) VALUES (?)", (skill_name,))
                        conn.execute(
                            "UPDATE skills SET total_calls = total_calls + 1 WHERE name = ?",
                            (skill_name,),
                        )
        except json.JSONDecodeError:
            continue

    # Update stats
    _update_session_stats(conn, sid)
    conn.commit()


def _update_session_stats(conn, sid: str):
    msg_count = conn.execute(
        "SELECT COUNT(*) FROM messages WHERE session_id = ?", (sid,)
    ).fetchone()[0]
    tool_count = conn.execute(
        "SELECT COUNT(*) FROM tool_calls WHERE session_id = ?", (sid,)
    ).fetchone()[0]
    conn.execute(
        """INSERT OR REPLACE INTO session_stats
           (session_id, message_count, tool_count, updated_at)
           VALUES (?, ?, ?, ?)""",
        (sid, msg_count, tool_count, datetime.now().isoformat()),
    )


def run_once(verbose: bool = False) -> dict:
    """Scan for new sessions and import them. DB is the source of truth."""
    conn = get_db()
    stats = {"claude": 0, "opencode": 0, "updated": 0, "skipped": 0}

    # --- Claude Code sessions ---
    claude_dirs = sorted(
        [d for d in SESSIONS.iterdir()
         if d.is_dir() and not d.name.startswith('.') and (d / "session.yaml").exists()]
    ) if SESSIONS.exists() else []

    # Get last DB state for Claude sessions
    db_sessions = set(
        r[0] for r in conn.execute("SELECT id FROM sessions WHERE ide='claude-code'").fetchall()
    ) if SESSIONS.exists() else set()

    # Get message counts from DB to detect new messages
    msg_counts = {}
    if SESSIONS.exists():
        for r in conn.execute(
            "SELECT session_id, COUNT(*) as cnt FROM messages GROUP BY session_id"
        ).fetchall():
            msg_counts[r["session_id"]] = r["cnt"]

    for session_dir in claude_dirs:
        sid = session_dir.name
        msgs_file = session_dir / "messages.jsonl"
        file_msg_count = 0
        if msgs_file.exists():
            file_msg_count = len(
                [l for l in msgs_file.read_text().strip().split("\n") if l.strip()]
            )

        if sid in db_sessions and file_msg_count <= msg_counts.get(sid, 0):
            stats["skipped"] += 1
            continue

        try:
            import_session(session_dir, conn)
            stats["claude" if sid not in db_sessions else "updated"] += 1
            if verbose:
                tag = "new" if sid not in db_sessions else "updated"
                print(f"  [claude] {tag} {sid}")
        except Exception as e:
            if verbose:
                print(f"  [claude] failed {sid}: {e}")

    # --- OpenCode sessions ---
    opencode_sessions = collect_new_opencode_sessions(conn)
    for session in opencode_sessions:
        try:
            import_opencode_session(session, conn)
            stats["opencode"] += 1
            if verbose:
                print(f"  [opencode] new {session['id']}")
        except Exception as e:
            if verbose:
                print(f"  [opencode] failed {session['id']}: {e}")

    conn.close()
    return stats


def run_daemon(interval: int = POLL_INTERVAL):
    """Run indefinitely, polling every `interval` seconds."""
    print(f"[daemon] Auto-import started (interval: {interval}s, {interval//60}min)")
    print(f"[daemon] Claude sessions: {SESSIONS}")
    print(f"[daemon] OpenCode DB: {OPCODE_DB}")

    while True:
        stats = run_once(verbose=True)
        total = stats["claude"] + stats["opencode"] + stats["updated"]
        print(f"[daemon] {datetime.now().strftime('%H:%M:%S')} "
              f"new_claude={stats['claude']} new_opencode={stats['opencode']} "
              f"updated={stats['updated']} skipped={stats['skipped']}")
        time.sleep(interval)
