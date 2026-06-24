"""Auto-import daemon: scan projects, import new sessions every 30 minutes."""
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
CHECKPOINT_FILE = BASE / "checkpoint.json"
POLL_INTERVAL = 1800  # 30 minutes


def load_checkpoint() -> set:
    """Return set of already-imported session IDs."""
    if not CHECKPOINT_FILE.exists():
        return set()
    try:
        data = json.loads(CHECKPOINT_FILE.read_text())
        return set(data.get("imported_sessions", []))
    except (json.JSONDecodeError, KeyError):
        return set()


def save_checkpoint(imported: set):
    CHECKPOINT_FILE.parent.mkdir(parents=True, exist_ok=True)
    CHECKPOINT_FILE.write_text(json.dumps({
        "last_run": datetime.now().isoformat(),
        "imported_sessions": list(imported),
        "count": len(imported),
    }, indent=2))


def collect_claude_sessions() -> list[Path]:
    """Find unimported Claude Code session directories from hooks."""
    if not SESSIONS.exists():
        return []
    return [
        d for d in sorted(SESSIONS.iterdir())
        if d.is_dir() and not d.name.startswith('.') and (d / "session.yaml").exists()
    ]


def collect_opencode_sessions() -> list[dict]:
    """Find OpenCode sessions from opencode.db."""
    if not OPCODE_DB.exists():
        return []
    try:
        conn = sqlite3.connect(str(OPCODE_DB))
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, title, model, cost, tokens_input, tokens_output, time_created "
            "FROM session WHERE title IS NOT NULL AND title != '' "
            "ORDER BY time_created DESC"
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]
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
        """INSERT OR IGNORE INTO sessions (id, ide, model, created_at, closed_at)
           VALUES (?, 'opencode', ?, ?, ?)""",
        (sid, session.get("model", ""), created, created),
    )

    # Import messages from part table
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
                conn.execute(
                    "INSERT OR IGNORE INTO tool_calls (session_id, call_id, tool, tool_type, args, seq_before, ts) VALUES (?, ?, ?, 'opencode', ?, ?, ?)",
                    (sid, f"oc-{sid}-{seq}", tool_name, tool_input, seq, str(ts)),
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

    conn.commit()


def run_once(verbose: bool = False) -> dict:
    """Scan for new sessions and import them. Returns stats."""
    conn = get_db()
    checkpoint = load_checkpoint()

    stats = {"claude_imported": 0, "opencode_imported": 0, "skipped": 0}

    # --- Claude Code sessions (hooks) ---
    claude_dirs = collect_claude_sessions()
    for session_dir in claude_dirs:
        sid = session_dir.name
        if sid in checkpoint:
            stats["skipped"] += 1
            continue
        try:
            import_session(session_dir, conn)
            checkpoint.add(sid)
            stats["claude_imported"] += 1
            if verbose:
                print(f"  [claude] imported {sid}")
        except Exception as e:
            if verbose:
                print(f"  [claude] failed {sid}: {e}")

    # --- OpenCode sessions ---
    opencode_sessions = collect_opencode_sessions()
    for session in opencode_sessions:
        sid = session["id"]
        if sid in checkpoint:
            stats["skipped"] += 1
            continue
        try:
            import_opencode_session(session, conn)
            checkpoint.add(sid)
            stats["opencode_imported"] += 1
            if verbose:
                print(f"  [opencode] imported {sid}")
        except Exception as e:
            if verbose:
                print(f"  [opencode] failed {sid}: {e}")

    save_checkpoint(checkpoint)
    conn.close()
    return stats


def run_daemon(interval: int = POLL_INTERVAL):
    """Run indefinitely, polling every `interval` seconds."""
    print(f"[daemon] Auto-import started (interval: {interval}s, {interval//60}min)")
    print(f"[daemon] Checkpoint: {CHECKPOINT_FILE}")
    print(f"[daemon] Claude sessions: {SESSIONS}")
    print(f"[daemon] OpenCode DB: {OPCODE_DB}")

    while True:
        stats = run_once(verbose=True)
        total = stats["claude_imported"] + stats["opencode_imported"]
        if total > 0 or stats["skipped"] > 0:
            print(f"[daemon] {datetime.now().strftime('%H:%M:%S')} "
                  f"claude={stats['claude_imported']} opencode={stats['opencode_imported']} "
                  f"skipped={stats['skipped']}")
        else:
            print(f"[daemon] {datetime.now().strftime('%H:%M:%S')} no new sessions")
        time.sleep(interval)
