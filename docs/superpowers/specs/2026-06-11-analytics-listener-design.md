# Analytics Listener — 设计文档

> 为 Claude Code 和 OpenCode 设计统一的 chat history / tool call / skill call 采集器，
> 本地 JSONL 存储 raw data，后续导入数据库分析。

## 1. 需求摘要

| 维度 | 选择 |
|------|------|
| 目的 | 使用分析 (Analytics) |
| 范围 | 本地个人使用 |
| 粒度 | 完整内容记录（chat 消息、tool 参数/结果） |
| 策略 | Claude Code + OpenCode 各自实现，统一存储格式 |
| 时间 | 本地时间 |

## 2. 整体架构

```
                    ~/.coworker/analytics/
                      sessions/{session-id}/
                        messages.jsonl
                        tools.jsonl
                        session.yaml
                      index.jsonl
                      hooks/              (Claude Code 脚本)
                        on-user-prompt.sh
                        on-pre-tool.sh
                        on-post-tool.sh
                        on-stop.sh
                   ↗                    ↖
           Claude Code Hooks      OpenCode Plugin
           (settings.json)        (.opencode/plugin)
```

- Claude Code: 通过 `.claude/settings.json` hooks 驱动 shell 脚本记录
- OpenCode: 通过 `@opencode-ai/plugin` SDK 驱动 TypeScript 记录
- 两者互不依赖，各自写入同一个本地目录
- 最终导入 SQLite/PostgreSQL 做分析（后续设计）

## 3. 数据模型

### 3.1 session.yaml — session 元数据

```yaml
session_id: "2026-06-11-T143052-a1b2c3"
created: "2026-06-11T14:30:52+08:00"
closed: "2026-06-11T15:45:10+08:00"
ide: opencode
project: ai-coworker
cwd: /home/cicidi/project/ai-coworker
```

### 3.2 messages.jsonl — chat 消息

每条消息一行 JSON：

```json
{"ts":"2026-06-11T14:30:52+08:00","type":"user","seq":1,"content":"帮我写一个 listener"}
{"ts":"2026-06-11T14:31:05+08:00","type":"assistant","seq":2,"content":"好的，让我先探索..."}
```

| 字段 | 说明 |
|------|------|
| `ts` | 本地时间，ISO 8601 + 时区 |
| `type` | `user` / `assistant` |
| `seq` | 全局自增序号 |
| `content` | 消息文本 |

### 3.3 tools.jsonl — tool call

每条一次 tool 调用，pre 和 post 分开写，各自独立：

```json
{"ts":"2026-06-11T14:31:05+08:00","phase":"before","tool":"bash","call_id":"toolu_01","seq":3,"args":{"command":"ls","description":"List files"}}
{"ts":"2026-06-11T14:31:10+08:00","phase":"after","tool":"bash","call_id":"toolu_01","seq":4,"result":"README.md\nsrc/","duration_ms":5230}
```

| 字段 | 说明 |
|------|------|
| `ts` | 本地时间 |
| `phase` | `before` / `after` |
| `tool` | tool 名称（Bash/Read/Write/Edit/Skill/Glob/Grep/TodoWrite/WebFetch...） |
| `call_id` | tool 调用 ID，关联 before 和 after |
| `seq` | 全局自增序号 |
| `args` | tool 参数（仅 before） |
| `result` | tool 返回结果（仅 after） |
| `duration_ms` | 执行耗时（仅 after） |

设计要点：
- pre 和 post 各自独立记录，谁触发谁写，互不依赖
- Claude Code 经常丢 pre 或 post hook — 这种设计下至少保留一半数据
- 按 `call_id` group 即可得到完整调用

### 3.4 index.jsonl — session 索引

每个 session 结束时追加一行：

```json
{"session_id":"a1b2c3","created":"2026-06-11T14:30:52+08:00","ide":"opencode","project":"ai-coworker","message_count":45,"tool_count":12}
```

## 4. Claude Code 实现

### 4.1 Hooks 配置

在 `.claude/settings.json` 中：

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "command": "~/.coworker/analytics/hooks/on-user-prompt.sh" }],
    "PreToolUse":       [{ "command": "~/.coworker/analytics/hooks/on-pre-tool.sh" }],
    "PostToolUse":      [{ "command": "~/.coworker/analytics/hooks/on-post-tool.sh" }],
    "Stop":             [{ "command": "~/.coworker/analytics/hooks/on-stop.sh" }]
  }
}
```

### 4.2 Hook 脚本职责

| Hook | 脚本 | 写入 |
|------|------|------|
| `UserPromptSubmit` | `on-user-prompt.sh` | `messages.jsonl`（type: user）+ 首次触发时创建 session |
| `PreToolUse` | `on-pre-tool.sh` | `tools.jsonl`（phase: before） |
| `PostToolUse` | `on-post-tool.sh` | `tools.jsonl`（phase: after） |
| `Stop` | `on-stop.sh` | 更新 `session.yaml` closed + 追加 `index.jsonl` |

### 4.3 Session ID 生成

首次 `UserPromptSubmit` 时生成：`$(date +%Y-%m-%d-T%H%M%S)-$(openssl rand -hex 3)`

## 5. OpenCode 实现

### 5.1 Plugin 结构

```
.opencode/coworker-analytics/
  index.ts          # 插件入口
  recorder.ts       # 核心写入逻辑
  session.ts        # 管理 session 生命周期
```

### 5.2 Hook 映射

| OpenCode Hook | 行为 |
|---------------|------|
| `event` | 监听 `session.created` → 创建 session 目录 + `session.yaml`；`session.deleted` → 更新 closed + 写 `index.jsonl` |
| `chat.message` | 每条消息 → `messages.jsonl` |
| `tool.execute.before` | → `tools.jsonl`（phase: before） |
| `tool.execute.after` | → `tools.jsonl`（phase: after） |

### 5.3 Recorder 核心

- `fs.appendFileSync` 追加写 JSONL
- 内存中的自增 `seq` 计数器
- 自动创建 session 目录

## 6. SQLite 数据库

> JSONL raw data 为采集阶段使用。导入 SQLite 后进行结构化分析。

### 6.1 表结构

```sql
CREATE TABLE sessions (
    id          TEXT PRIMARY KEY,
    ide         TEXT NOT NULL,
    project     TEXT,
    cwd         TEXT,
    model       TEXT,
    created_at  TEXT NOT NULL,
    closed_at   TEXT
);

CREATE TABLE messages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    seq         INTEGER NOT NULL,
    type        TEXT NOT NULL,
    content     TEXT NOT NULL,
    ts          TEXT NOT NULL
);
CREATE INDEX idx_messages_session ON messages(session_id);

CREATE TABLE tool_calls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  TEXT NOT NULL REFERENCES sessions(id),
    call_id     TEXT NOT NULL,
    tool        TEXT NOT NULL,
    args        TEXT,
    result      TEXT,
    duration_ms INTEGER,
    seq_before  INTEGER,
    seq_after   INTEGER,
    ts          TEXT NOT NULL
);
CREATE INDEX idx_tool_calls_session ON tool_calls(session_id);
CREATE INDEX idx_tool_calls_tool ON tool_calls(tool);
```

### 6.2 分析视图

```sql
CREATE VIEW skill_calls AS
SELECT * FROM tool_calls WHERE tool = 'Skill';

CREATE VIEW planning AS
SELECT * FROM tool_calls WHERE tool = 'TodoWrite';

CREATE VIEW session_stats AS
SELECT
    s.id,
    s.ide,
    s.project,
    s.created_at,
    s.closed_at,
    COUNT(DISTINCT m.id) AS message_count,
    COUNT(DISTINCT t.id) AS tool_count,
    COUNT(DISTINCT CASE WHEN t.tool = 'Skill' THEN t.id END) AS skill_count
FROM sessions s
LEFT JOIN messages m ON m.session_id = s.id
LEFT JOIN tool_calls t ON t.session_id = s.id
GROUP BY s.id;
```

### 6.3 导入逻辑

```
JSONL files → Python/Go 脚本 → SQLite
```

pre+post 合并：按 `call_id` group，两条时合并为一行（args + result + duration_ms），只有一条时保留部分数据。

## 7. 安装

`setup/install.sh` 负责：

1. 创建 `~/.coworker/analytics/sessions/` 目录
2. 复制 4 个 hook 脚本到 `~/.coworker/analytics/hooks/`
3. 将 hooks 配置 merge 到项目的 `.claude/settings.json`
4. 创建 SQLite 数据库 `~/.coworker/analytics/analytics.db` 并执行 DDL

OpenCode 侧无需安装 —— plugin 随 `.opencode/` 目录自带。

## 8. 错误处理

核心原则：listener 出错不影响 AI 正常工作。

| 场景 | 策略 |
|------|------|
| 磁盘满 | 静默失败，不阻塞 AI |
| 权限不足 | 写 `~/.coworker/analytics/.errors.log`，不抛异常 |
| 数据格式异常 | 写 raw 数据到 `.errors.log`，跳过该条 |
| 并发写入 | JSONL 的 O_APPEND 原子操作天然安全 |
| 目录不存在 | recorder 自动创建 |

所有 hook 脚本和 plugin 入口均使用 try-catch + 静默降级。

## 9. 测试策略

手工验证流程：

1. 启动一次 AI 会话（Claude Code 或 OpenCode）
2. 进行若干操作（发送消息、调用 tool、使用 skill）
3. 结束会话
4. 检查 `~/.coworker/analytics/sessions/` 下是否生成正确的文件
5. 验证 JSONL 每行都是合法 JSON，时间戳正确，seq 自增不跳
