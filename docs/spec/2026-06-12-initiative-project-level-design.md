# Initiative 从 Global → Project-Level — 设计文档

> **SUPERSEDED on 2026-07-02**: This design was reversed. Initiatives are now stored GLOBALLY at `~/.coworker/initiatives/` (not project-level). The storage spec below is kept for historical reference. See `src/coworker/config.py:INITIATIVES_DIR` and `coworker-blueprint.md §7` for the current global model.

## 1. 需求

Initiative（工作语境）从全局改为项目级：
- 每个 project 管理自己的 initiatives
- Dashboard 只显示当前 project + initiative 的数据
- Initiative 通过项目 git 提交自然共享，删除 publish/import

## 2. 存储变更

| 项目 | 之前 | 之后 |
|------|------|------|
| Initiative YAML | `~/.coworker/initiatives/<name>.yaml` | `{project}/.coworker/initiatives/<name>.yaml` |
| Create/Edit/Remove | 全局目录操作 | 项目内操作 |
| 活跃 Initiative | 注入到 CLAUDE.md (不变) | 注入到当前 project 的 CLAUDE.md |

## 3. 代码修改清单

### 3.1 config.py

```python
# 之前
INITIATIVES_DIR = GLOBAL_DIR / "initiatives"

# 之后 — 改为函数，接受 project_dir
def get_initiatives_dir(project_dir: Path | None = None) -> Path:
    p = Path(project_dir) if project_dir else Path.cwd()
    return p / ".coworker" / "initiatives"
```

`list_initiatives`, `load_initiative`, `save_initiative`, `initiative_exists` 全部加 `project_dir` 参数。

### 3.2 models.py

删除 `InitiativeConfig.source: ImportSource | None` 字段。

### 3.3 manager.py

```python
class InitiativeManager:
    def __init__(self, project_dir: Path | None = None):
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()
        self.initiatives_dir = self.project_dir / ".coworker" / "initiatives"
```

- `create()` — 在 `self.initiatives_dir` 创建
- `edit()` — 从 `self.initiatives_dir` 读/写
- `activate()` — `_resolve_target_dirs()` 简化为只返回 `self.project_dir`
- `deactivate()` — 只清理 `self.project_dir` 的文件
- `list_all()` — 只列 `self.initiatives_dir` 下的
- `remove()` — 从 `self.initiatives_dir` 删除
- **删除** `publish()`, `import_from_url()` 方法

### 3.4 cli.py

所有 initiative 命令加 `--project`:

```python
@click.option("--project", "-p", default=None, help="Project directory (default: current)")
```

默认值 `os.getcwd()`。删除 `publish` 和 `import` 命令。

### 3.5 adapters/claude.py + opencode.py

`inject_initiative()` / `remove_initiative()` 不需要改（已经接受 `project_dir` 参数，作用在 project-level 文件）。

### 3.6 skills/initiative-create/SKILL.md + initiative-edit/SKILL.md

更新文档中的 CLI 示例，加上 `--project` 参数，删除 publish/import 引用。

### 3.7 Dashboard — 前端

- 加 project 下拉 filter（Overview 页面顶部）
- `/api/projects` 新 endpoint：返回所有 unique project 名
- Sessions/Initiatives 视图已有 project 列，无需改查询逻辑

### 3.8 setup/install.sh

移除 global initiatives 目录初始化。

## 4. 删除项

| 项目 | 理由 |
|------|------|
| `coworker initiative publish` | git 提交共享 |
| `coworker initiative import` | 不需要跨项目 import |
| `InitiativeConfig.source` | 不再追踪 import 来源 |
| `manager.py:publish()`, `manager.py:import_from_url()` | 对应 CLI 删除 |

## 5. 改动量估算

| 文件 | 改动行数 | 类型 |
|------|---------|------|
| `src/coworker/config.py` | ~20 | 函数签名加参数 |
| `src/coworker/models.py` | ~5 | 删除 source 字段 |
| `src/coworker/initiatives/manager.py` | ~80 | 删除 publish/import，project_dir 参数 |
| `src/coworker/cli.py` | ~30 | 加 --project，删 publish/import 命令 |
| `src/coworker/adapters/claude.py` | ~0 | 不需要改 |
| `src/coworker/adapters/opencode.py` | ~0 | 不需要改 |
| `skills/initiative-create/SKILL.md` | ~10 | 更新文档 |
| `skills/initiative-edit/SKILL.md` | ~10 | 更新文档 |
| `static/dashboard.js` | ~20 | 加 project filter |
| `src/coworker/dashboard/queries.py` | ~5 | 加 /api/projects query |
| `src/coworker/dashboard/app.py` | ~3 | 加 route |
| `tests/python/test_config.py` | ~10 | 更新测试 |
| `setup/install.sh` | ~1 | 删除全局 init dir |
| **合计** | **~194** | 改动量小 |

## 6. 测试计划

1. `test_initiative_project_scoped` — 验证 initiative 创建在 project 目录下
2. `test_initiative_activate_single_project` — 验证 activate 只注入当前 project
3. `test_initiative_list_project_only` — 验证 list 只列出当前 project 的
4. `test_dashboard_project_filter` — 验证 /api/projects 返回正确数据
5. 回归：所有现有测试继续通过

## 7. Dashboard 新 API

```python
@app.get("/api/projects")
def api_projects():
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT project FROM sessions WHERE project IS NOT NULL AND project != '' ORDER BY project"
    ).fetchall()
    conn.close()
    return [r["project"] for r in rows]
```
