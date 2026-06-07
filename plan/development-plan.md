# Development Plan

Step-by-step guide for building **Python Agentic Workbench**. Each phase ends with a checkpoint you can verify before moving on.

Reference: [overview.md](./overview.md)

---

## How to Use This Plan

1. Complete phases in order — later phases depend on earlier ones.
2. Check off each step as you finish it.
3. Run the **Checkpoint** at the end of every phase before continuing.
4. Write tests after each milestone (Phase 0 sets up pytest).
5. Keep modules small, use type hints, and never hardcode secrets.
6. Use [uv](https://docs.astral.sh/uv/) for environment and dependency management. Prefix commands with `uv run` (e.g. `uv run pytest`) so you don't need to activate the venv manually.

**Estimated pace:** 1–2 phases per week if working part-time; adjust as needed.

---

## Phase 0: Project Setup

**Goal:** A runnable Python package with dev tooling in place.

### Steps

- [x] **0.1** Create a virtual environment (if not already done):
  ```bash
  uv venv
  ```
  `uv sync` in step 0.6 also creates `.venv` if it is missing, so this step is optional.

- [x] **0.2** Create `pyproject.toml` with:
  - Project name: `python-agentic-workbench`
  - Python version: `>=3.11`
  - `[dependency-groups]` dev: `pytest`, `httpx`, `python-dotenv`, `typer` (or use stdlib `argparse` later)
  - `[tool.uv] package = true` so `uv sync` installs the project in editable mode
  - Console script entry point placeholder: `workbench = workbench.cli:app`

- [x] **0.3** Create the package skeleton:
  ```text
  workbench/
    __init__.py
    cli.py
  tests/
    __init__.py
  reports/
    .gitkeep
  ```

- [x] **0.4** Add `.env.example` with placeholder keys (e.g. `OPENAI_API_KEY=`, `OLLAMA_BASE_URL=`).

- [x] **0.5** Update `.gitignore` to include:
  - `.venv/`, `__pycache__/`, `*.pyc`, `.env`, `tasks.json`, `reports/*.md`, `reports/*.json`

- [x] **0.6** Install the package in editable mode with dev dependencies:
  ```bash
  uv sync --group dev
  ```

- [x] **0.7** Add a smoke test `tests/test_smoke.py` that imports `workbench` and passes.

### Checkpoint

```bash
uv run pytest -v
uv run python -c "import workbench; print('ok')"
```

Both commands succeed.

---

## Phase 1: Basic Task Manager CLI

**Goal:** A working task manager that persists to `tasks.json`.

**Concepts:** variables, functions, lists/dicts, loops, conditionals, JSON I/O, basic error handling.

### Steps

- [x] **1.1** Create `workbench/stores/json_store.py` with generic helpers:
  - `load_json(path: Path) -> list | dict`
  - `save_json(path: Path, data) -> None`
  - Handle missing file (return empty list) and invalid JSON (raise readable error).

- [x] **1.2** Create `workbench/services/task_service.py` (simple version first — no classes yet):
  - `TASKS_FILE = Path("tasks.json")`
  - `add_task(title: str) -> dict`
  - `list_tasks() -> list[dict]`
  - `complete_task(task_id: int) -> dict`
  - `delete_task(task_id: int) -> None`
  - Each task dict: `{ "id", "title", "completed" }`

- [x] **1.3** Create a minimal `workbench/cli.py` with a simple menu loop (temporary — replaced in Phase 3):
  - Options: add, list, complete, delete, quit
  - Read user input from `input()`

- [x] **1.4** Wire `main.py` or the CLI entry point to call the menu loop.

- [x] **1.5** Manually test all four operations; confirm `tasks.json` persists after restart.

### Checkpoint

- [x] Add a task from the terminal.
- [x] List all saved tasks.
- [x] Mark a task complete.
- [x] Delete a task.
- [x] Quit and relaunch — data is still there.

---

## Phase 2: Domain Models and Services

**Goal:** Refactor raw dicts into structured models with separated storage and business logic.

**Concepts:** classes, dataclasses, type hints, separation of concerns, service layer.

### Steps

- [ ] **2.1** Create `workbench/models/task.py`:
  ```python
  @dataclass
  class Task:
      id: int
      title: str
      status: str          # "open" | "done"
      priority: str        # "low" | "medium" | "high"
      created_at: datetime
      completed_at: datetime | None = None
  ```

- [ ] **2.2** Create `workbench/models/project.py`:
  ```python
  @dataclass
  class Project:
      id: int
      name: str
      created_at: datetime
  ```

- [ ] **2.3** Create `workbench/stores/task_store.py`:
  - `TaskStore` class wrapping JSON persistence
  - Methods: `load_all()`, `save_all(tasks)`, `load_projects()`, `save_projects(projects)`
  - Serialize/deserialize dataclasses to/from dicts

- [ ] **2.4** Refactor `workbench/services/task_service.py`:
  - `TaskService(store: TaskStore)` class
  - Move all business logic here; no direct file I/O in the service
  - Add `create`, `list`, `complete`, `delete` methods returning `Task` objects

- [ ] **2.5** Create `workbench/services/project_service.py`:
  - `ProjectService(store: TaskStore)` with `create(name)` and `list()`

- [ ] **2.6** Update the CLI menu to use the new service classes.

- [ ] **2.7** Write `tests/test_json_store.py` and `tests/test_task_service.py`:
  - Test add/complete/delete round-trip
  - Test missing file handling
  - Test invalid task ID

### Checkpoint

```bash
uv run pytest tests/test_json_store.py tests/test_task_service.py -v
```

- [ ] Task creation goes through `TaskService`.
- [ ] Storage goes through `TaskStore`.
- [ ] Data still persists as JSON.
- [ ] Code lives in separate modules under `models/`, `stores/`, `services/`.

---

## Phase 3: Proper CLI Interface

**Goal:** Replace the menu loop with a real nested CLI and package entry point.

**Concepts:** CLI routing, arguments, options, entry points, terminal UX.

### Steps

- [ ] **3.1** Choose CLI library: **Typer** (recommended) or `argparse`.

- [ ] **3.2** Rewrite `workbench/cli.py` with nested commands:
  ```bash
  workbench task add "Learn async Python"
  workbench task list
  workbench task complete 3
  workbench task delete 2
  workbench project create my-project
  workbench project list
  ```

- [ ] **3.3** Add `--help` to every command and subcommand.

- [ ] **3.4** Add input validation:
  - Reject empty task titles
  - Show clear error for unknown task IDs
  - Exit with non-zero code on failure

- [ ] **3.5** Register the console script in `pyproject.toml`:
  ```toml
  [project.scripts]
  workbench = "workbench.cli:app"
  ```

- [ ] **3.6** Re-sync the editable package and verify the CLI is on PATH:
  ```bash
  uv sync --group dev
  uv run workbench --help
  ```

- [ ] **3.7** Add CLI integration tests (optional but recommended):
  - Use `typer.testing.CliRunner` or subprocess calls

### Checkpoint

```bash
uv run workbench --help
uv run workbench task add "Test task"
uv run workbench task list
uv run workbench task complete 1
uv run workbench project create demo
```

- [ ] Nested commands work.
- [ ] Help text is readable.
- [ ] Invalid input produces clear errors.

---

## Phase 4: File System Scanner

**Goal:** Scan a local directory and produce a Markdown report.

**Concepts:** `pathlib`, recursive traversal, string parsing, Markdown generation, ignore rules.

### Steps

- [ ] **4.1** Create `workbench/core/config.py` with default ignore dirs:
  ```python
  DEFAULT_IGNORE = {".git", "node_modules", ".venv", "dist", "build", "__pycache__"}
  ```

- [ ] **4.2** Create `workbench/models/report.py`:
  - `ScanResult` dataclass: root path, file counts by extension, todo items, total files

- [ ] **4.3** Create `workbench/services/scan_service.py`:
  - `ScanService.scan(path: Path) -> ScanResult`
  - Walk directory tree with `pathlib.Path.rglob` or `os.walk`
  - Skip ignored directories
  - Count files by extension
  - Extract `TODO` and `FIXME` comments from source files (regex on line content)

- [ ] **4.4** Create `workbench/services/report_service.py`:
  - `ReportService.write_scan_markdown(result: ScanResult, output: Path) -> None`
  - Sections: summary, extension breakdown, TODO/FIXME list

- [ ] **4.5** Add CLI command:
  ```bash
  workbench scan ./some-project
  workbench scan ./some-project --output reports/scan-report.md
  ```

- [ ] **4.6** Print a terminal summary (file count, top extensions, TODO count) before writing the report.

- [ ] **4.7** Write `tests/test_scan_service.py`:
  - Create a temp directory with sample files and TODOs
  - Assert ignore rules work
  - Assert TODO extraction finds expected items

### Checkpoint

```bash
uv run workbench scan .
```

- [ ] Scanner summarizes the repo in the terminal.
- [ ] Markdown report is written to `reports/`.
- [ ] `.git`, `node_modules`, `.venv` are ignored.
- [ ] TODO/FIXME comments appear in the report.

---

## Phase 5: API Client Layer

**Goal:** A reusable HTTP client with timeout, retry, and env-based secrets.

**Concepts:** HTTP requests, environment variables, custom exceptions, response parsing.

### Steps

- [ ] **5.1** Create `workbench/core/errors.py`:
  - `WorkbenchError` (base)
  - `ApiError`, `TimeoutError`, `ConfigError`

- [ ] **5.2** Create `workbench/core/config.py` additions:
  - Load `.env` via `python-dotenv`
  - `get_env(key: str, required: bool = False) -> str | None`

- [ ] **5.3** Create `workbench/integrations/http_client.py`:
  - `HttpClient` class using `httpx`
  - `get(url, params, headers, timeout) -> dict`
  - Configurable timeout (default 10s)
  - Retry on transient failures (e.g. 3 attempts with backoff)
  - Raise `ApiError` on 4xx/5xx with response body snippet

- [ ] **5.4** Add a demo CLI command to prove it works:
  ```bash
  workbench api ping   # calls a public API like https://httpbin.org/get
  ```

- [ ] **5.5** Write tests with `httpx` mock transport or `pytest-httpx`:
  - Success response parsing
  - Timeout handling
  - Retry on 503

### Checkpoint

```bash
uv run workbench api ping
```

- [ ] Public API call succeeds.
- [ ] Timeout produces a readable error (test with a slow/unreachable URL).
- [ ] No secrets in source code — only in `.env`.

---

## Phase 6: Async Execution

**Goal:** Run concurrent file and API operations with `asyncio`.

**Concepts:** `async`/`await`, concurrent execution, async error handling.

### Steps

- [ ] **6.1** Create async version of HTTP client: `workbench/integrations/async_http_client.py`
  - Use `httpx.AsyncClient`
  - `async def get(...)`, `async def get_many(urls) -> list`

- [ ] **6.2** Create `workbench/services/async_scan_service.py`:
  - `async def scan_files(paths: list[Path]) -> list[ScanResult]`
  - Process multiple directories concurrently

- [ ] **6.3** Create a simple async task queue in `workbench/core/task_queue.py`:
  - Accept a list of coroutines
  - Run with `asyncio.gather(..., return_exceptions=True)`
  - Collect successes and failures separately

- [ ] **6.4** Add CLI command:
  ```bash
  workbench scan-async ./proj-a ./proj-b
  ```

- [ ] **6.5** Write tests for concurrent execution and partial failure handling.

### Checkpoint

- [ ] Multiple API calls run concurrently (log timestamps to verify).
- [ ] One failed task does not crash the whole batch.
- [ ] Results collected into a structured object (list of results + list of errors).

---

## Phase 7: Tool Registry

**Goal:** Register callable tools and execute them by name — the foundation for the agent loop.

**Concepts:** function references, tool metadata, dynamic dispatch, input validation.

### Steps

- [ ] **7.1** Create `workbench/models/tool.py`:
  ```python
  @dataclass
  class Tool:
      name: str
      description: str
      func: Callable
      parameters: dict   # JSON-schema-like description
  ```

- [ ] **7.2** Create tool implementations:
  - `workbench/tools/file_tools.py` → `list_files`, `read_file`
  - `workbench/tools/search_tools.py` → `search_text`
  - `workbench/tools/api_tools.py` → `fetch_url`
  - `workbench/tools/report_tools.py` → `write_report`

- [ ] **7.3** Create `workbench/tools/registry.py`:
  ```python
  class ToolRegistry:
      def register(self, tool: Tool) -> None
      def get(self, name: str) -> Tool
      def list_tools(self) -> list[Tool]
      def execute(self, name: str, **kwargs) -> Any
  ```
  - Validate required parameters before calling
  - Log every execution (tool name, args, result summary)

- [ ] **7.4** Register all tools in `workbench/tools/__init__.py`.

- [ ] **7.5** Add CLI command:
  ```bash
  workbench tool list
  workbench tool run list_files --path .
  workbench tool run search_text --path . --query "TODO"
  ```

- [ ] **7.6** Write `tests/test_tool_registry.py`:
  - Register and execute a tool
  - Unknown tool name raises clear error
  - Missing required param raises validation error

### Checkpoint

```bash
uv run workbench tool list
uv run workbench tool run read_file --path README.md
```

- [ ] Tools registered in one place.
- [ ] Tools callable by name.
- [ ] Invalid calls return useful errors.
- [ ] Executions are logged.

---

## Phase 8: Agentic Planning Loop (No LLM)

**Goal:** A deterministic agent that plans, selects tools, executes, observes, and reports.

**Concepts:** workflow orchestration, state management, planning loops, execution history.

### Steps

- [ ] **8.1** Create `workbench/agent/memory.py`:
  - `AgentMemory` class storing observations and action history
  - Methods: `add_observation(step, tool, result)`, `get_history()`

- [ ] **8.2** Create `workbench/agent/planner.py`:
  - `Planner.create_plan(goal: str) -> list[PlanStep]`
  - Start with **rule-based** planning (no LLM):
    - If goal mentions "scan" → plan: `list_files`, `search_text`, `write_report`
    - If goal mentions "todo" → plan: `search_text` with query "TODO"

- [ ] **8.3** Create `workbench/agent/executor.py`:
  - `Executor.run_step(step, registry) -> StepResult`
  - Catch tool errors; store in memory; continue or halt based on severity

- [ ] **8.4** Create `workbench/agent/loop.py`:
  ```python
  class AgentLoop:
      def run(self, goal: str) -> AgentResult:
          plan = planner.create_plan(goal)
          for step in plan:
              result = executor.run_step(step, registry)
              memory.add_observation(...)
          return agent_result
  ```

- [ ] **8.5** Add CLI command:
  ```bash
  workbench agent run "scan this repo for TODOs"
  ```

- [ ] **8.6** Final output includes: goal, plan steps, actions taken, results found.

- [ ] **8.7** Write `tests/test_agent_loop.py`:
  - Agent executes multiple tool steps
  - Each step appears in history
  - Final report contains expected sections

### Checkpoint

```bash
uv run workbench agent run "find all TODO comments in this project"
```

- [ ] Agent executes multiple tool steps.
- [ ] Each step is logged.
- [ ] Final output lists actions and results.

---

## Phase 9: LLM Integration

**Goal:** Connect the agent loop to an LLM for planning and tool selection.

**Concepts:** LLM API usage, structured outputs, tool calling, guardrails, response validation.

### Steps

- [ ] **9.1** Create `workbench/integrations/llm_client.py`:
  - Abstract base: `LLMClient.complete(prompt, tools) -> LLMResponse`
  - Response schema: `{ plan: [...], tool_calls: [...], summary: str }`

- [ ] **9.2** Implement one provider first (pick one):
  - `workbench/integrations/openai_client.py` — OpenAI API
  - **or** `workbench/integrations/ollama_client.py` — local Ollama

- [ ] **9.3** Add LLM config to `.env.example`:
  ```
  OPENAI_API_KEY=sk-...
  OPENAI_MODEL=gpt-4o-mini
  # or
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_MODEL=llama3
  ```

- [ ] **9.4** Update `workbench/agent/planner.py`:
  - Add `LLMPlanner` that sends goal + available tools to the model
  - Parse structured JSON response
  - Validate response against a schema (required fields, known tool names)

- [ ] **9.5** Add guardrails in `workbench/agent/executor.py`:
  - **Dangerous tools** (e.g. `write_report`, any file write) require `--confirm` flag
  - Reject tool calls with unknown names or invalid args
  - Log all LLM requests and responses (redact API keys)

- [ ] **9.6** Add CLI commands:
  ```bash
  workbench agent llm-run "summarize the architecture of this repo"
  workbench agent llm-run "write a report" --confirm
  ```

- [ ] **9.7** Write tests (mock LLM responses):
  - Valid plan is parsed and executed
  - Invalid tool name is rejected
  - Write operations blocked without confirmation

### Checkpoint

- [ ] LLM creates a plan from a natural-language goal.
- [ ] LLM can request tool execution.
- [ ] Tool calls validated before running.
- [ ] Dangerous operations require `--confirm`.

---

## Phase 10: Repo Review Agent (Capstone)

**Goal:** The full `workbench review ./repo` command with JSON and Markdown reports.

**Concepts:** end-to-end design, agentic orchestration, structured reporting, LLM-assisted reasoning.

### Steps

- [ ] **10.1** Extend `workbench/models/report.py`:
  ```python
  @dataclass
  class RepoReviewReport:
      repo_path: str
      summary: str
      file_tree: str
      languages: dict[str, int]
      frameworks: list[str]
      todos: list[TodoItem]
      large_files: list[FileInfo]
      risk_areas: list[str]
      refactor_suggestions: list[str]
      test_suggestions: list[str]
      recommendation: str
  ```

- [ ] **10.2** Create `workbench/services/review_service.py`:
  - Orchestrate: scan → analyze → LLM summarize → build report
  - Detect languages from file extensions
  - Detect frameworks from config files (`pyproject.toml`, `package.json`, etc.)
  - Flag large files (> threshold, e.g. 500 lines or 100 KB)
  - Identify risk areas (many TODOs, large files, missing tests)

- [ ] **10.3** Extend `workbench/services/report_service.py`:
  - `write_review_json(report, path)`
  - `write_review_markdown(report, path)`

- [ ] **10.4** Wire the full agent loop:
  1. Accept repo path
  2. Run scan tools
  3. Send findings to LLM for analysis and recommendations
  4. Merge structured data + LLM insights into `RepoReviewReport`
  5. Write both output files

- [ ] **10.5** Add CLI command:
  ```bash
  workbench review ./path-to-repo
  workbench review ./path-to-repo --output-dir reports/
  ```

- [ ] **10.6** Output files:
  ```text
  reports/
    repo-review.json
    repo-review.md
  ```

- [ ] **10.7** Report sections (Markdown):
  - Repository summary
  - File tree overview
  - Detected languages and frameworks
  - TODO/FIXME findings
  - Large files
  - Potential risk areas
  - Suggested refactor tasks
  - Suggested test coverage improvements
  - Final recommendation

- [ ] **10.7** Add end-to-end test:
  - Run review on a small fixture repo
  - Assert both JSON and Markdown files exist
  - Assert key sections present

### Checkpoint

```bash
uv run workbench review .
ls reports/
cat reports/repo-review.md
```

- [ ] Review works on any local repo.
- [ ] Both Markdown and JSON reports generated.
- [ ] Report includes actionable recommendations.
- [ ] Process is repeatable and logged.

---

## Phase 11: Polish and Hardening

**Goal:** Production-quality developer tool feel.

### Steps

- [ ] **11.1** Add structured logging in `workbench/core/logging.py`:
  - Use stdlib `logging` module
  - `--verbose` / `--quiet` CLI flags

- [ ] **11.2** Review all modules for type hint coverage (`mypy` optional).

- [ ] **11.3** Ensure full test suite passes:
  ```bash
  uv run pytest -v --cov=workbench
  ```

- [ ] **11.4** Update `README.md` with:
  - Install instructions (`uv sync --group dev`)
  - All CLI commands with examples
  - Environment variable reference
  - Example report output

- [ ] **11.5** Add a `Makefile` or `justfile` with common commands:
  ```makefile
  install: uv sync --group dev
  test:  uv run pytest -v
  lint:  uv run ruff check workbench tests
  review: uv run workbench review .
  ```

### Checkpoint

```bash
make test
uv run workbench review . --output-dir reports/
```

Full test suite green. README matches actual behavior.

---

## Quick Reference: Build Order


| Phase | Milestone         | Key Deliverable                      |
| ----- | ----------------- | ------------------------------------ |
| 0     | Setup             | Package skeleton + pytest            |
| 1     | Task Manager      | JSON-backed task CRUD                |
| 2     | Models & Services | Dataclasses + service/store split    |
| 3     | CLI               | `workbench task/project` commands    |
| 4     | File Scanner      | `workbench scan` + Markdown report   |
| 5     | API Client        | HTTP client with retry + env secrets |
| 6     | Async             | Concurrent scan/API operations       |
| 7     | Tool Registry     | Register and execute tools by name   |
| 8     | Agent Loop        | Rule-based plan → execute → report   |
| 9     | LLM Integration   | LLM-driven planning + guardrails     |
| 10    | Repo Review       | `workbench review` capstone          |
| 11    | Polish            | Logging, tests, docs                 |


---

## Stretch Goals (After Phase 11)

Pick these up only after the capstone works end-to-end:

- [ ] Web UI with FastAPI
- [ ] SQLite storage backend
- [ ] Plugin-based tool registry
- [ ] Repo memory / vector search over files
- [ ] GitHub remote repo review
- [ ] Pull request review mode
- [ ] Docker support
- [ ] CI pipeline (GitHub Actions)
- [ ] HTML report dashboard
- [ ] Multi-agent reviewer system

---

## Tips While Building

1. **Commit after each phase checkpoint** — small, working increments.
2. **Don't skip tests** — they catch regressions when refactoring in later phases.
3. **Keep the CLI working** — even mid-refactor, one command should always run.
4. **Read the logs** — when the agent misbehaves in Phases 8–10, logs are your debugger.
5. **Start with one LLM provider** — get OpenAI *or* Ollama working before supporting both.

