# Python Agentic Workbench

## 1. Project Overview

**Python Agentic Workbench** is a learning-oriented Python project designed to build practical Python fluency through a real automation and agentic API workflow.

The project starts as a local CLI task manager and gradually evolves into a repo analysis agent capable of scanning codebases, calling tools, using structured data models, integrating with APIs, running async workflows, and producing machine-readable reports.

The goal is not to learn Python syntax in isolation, but to build operational Python skill through a complete, extensible system.

---

## 2. Primary Learning Goals

By completing this project, the developer should gain hands-on experience with:

- Python project structure
- Functions, modules, imports
- Classes and object-oriented design
- Dataclasses and/or Pydantic models
- File system operations
- JSON and Markdown generation
- CLI application development
- Error handling and logging
- API clients
- Async programming
- Tool registry design
- Agentic planning loops
- LLM API integration
- Testing with pytest
- Packaging and execution as a local developer tool

---

## 3. Final Product Vision

The final application should expose a CLI command:

```bash
workbench review ./path-to-repo
```

The command should analyze a repository and generate:

- Architecture summary
- File tree summary
- Detected tech stack
- TODO/FIXME list
- Risk areas
- Suggested refactor tasks
- Markdown report
- JSON report

---

## 4. Milestone Breakdown

## Milestone 1: Basic Task Manager CLI

### Objective

Build a simple CLI-based task manager backed by a JSON file.

### Features

- Add task
- List tasks
- Mark task as complete
- Delete task
- Persist tasks in `tasks.json`

### Concepts Practiced

- Variables
- Functions
- Lists and dictionaries
- Loops
- Conditionals
- File read/write
- JSON serialization
- Basic error handling

### Acceptance Criteria

- User can add a task from the terminal.
- User can list all saved tasks.
- User can mark a task as complete.
- User can delete a task.
- Task data persists after the program exits.

---

## Milestone 2: Domain Models and Services

### Objective

Refactor the task manager into a more structured Python application.

### Required Models

- `Task`
- `Project`
- `TaskStore`
- `TaskService`

### Features

- Replace raw dictionaries with structured models.
- Separate storage logic from business logic.
- Add task status, priority, and timestamps.

### Concepts Practiced

- Classes
- Dataclasses
- Type hints
- Separation of concerns
- Service layer design

### Acceptance Criteria

- Task creation is handled through a service class.
- Storage is handled through a separate store class.
- Data is still persisted as JSON.
- Code is split into multiple modules.

---

## Milestone 3: Proper CLI Interface

### Objective

Replace ad-hoc terminal input with a real CLI interface.

### Recommended Libraries

- `argparse`
- or `typer`

### Example Commands

```bash
workbench task add "Learn async Python"
workbench task list
workbench task complete 3
workbench project create appraise-python-lab
```

### Concepts Practiced

- CLI command routing
- Arguments
- Options
- Package entry points
- Terminal UX

### Acceptance Criteria

- CLI supports nested commands.
- Commands have help text.
- Invalid input produces readable errors.

---

## Milestone 4: File System Scanner

### Objective

Add the ability to scan a local folder or repository.

### Command

```bash
workbench scan ./some-project
```

### Features

- Walk through a directory tree.
- Ignore common folders:
  - `.git`
  - `node_modules`
  - `.venv`
  - `dist`
  - `build`

- Count files by extension.
- Extract TODO/FIXME comments.
- Generate a Markdown scan report.

### Concepts Practiced

- `pathlib`
- Recursive directory traversal
- String parsing
- Markdown generation
- Ignore rules

### Acceptance Criteria

- Scanner can summarize a repository.
- Scanner ignores configured folders.
- Scanner outputs both terminal summary and Markdown report.

---

## Milestone 5: API Client Layer

### Objective

Add support for calling external APIs.

### Features

- Create a reusable HTTP client.
- Support GET requests.
- Add timeout handling.
- Add retry logic.
- Read API keys from environment variables.
- Parse JSON responses.

### Recommended Libraries

- `httpx`
- `python-dotenv`

### Concepts Practiced

- HTTP requests
- Environment variables
- API error handling
- Custom exceptions
- Response parsing

### Acceptance Criteria

- API client can call a public API.
- Timeout and failure cases are handled cleanly.
- Secrets are not hardcoded.

---

## Milestone 6: Async Execution

### Objective

Introduce async workflows for concurrent file/API operations.

### Features

- Async API fetching
- Concurrent file processing
- Timeout handling
- Simple task queue

### Concepts Practiced

- `asyncio`
- `async` / `await`
- Concurrent execution
- Async error handling

### Acceptance Criteria

- Multiple API calls can run concurrently.
- Async workflow does not crash on one failed task.
- Results are collected into a structured object.

---

## Milestone 7: Tool Registry

### Objective

Build a simple tool system similar to what agent frameworks use internally.

### Example Tools

- `list_files`
- `read_file`
- `search_text`
- `write_report`
- `fetch_url`
- `summarize_text`

### Example Registry

```python
TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "search_text": search_text,
}
```

### Concepts Practiced

- Function references
- Tool metadata
- Dynamic dispatch
- Input validation
- Controlled execution

### Acceptance Criteria

- Tools can be registered in one place.
- Tools can be called by name.
- Invalid tool calls return useful errors.
- Tool results are logged.

---

## Milestone 8: Agentic Planning Loop

### Objective

Build a basic agent loop without relying on an LLM at first.

### Flow

```text
Goal
→ Create plan
→ Select tool
→ Execute tool
→ Observe result
→ Decide next action
→ Produce final output
```

### Features

- Accept a user goal.
- Generate a simple step-by-step plan.
- Execute tools from the registry.
- Store observations.
- Produce final report.

### Concepts Practiced

- Workflow orchestration
- State management
- Planning loops
- Tool execution history
- Report generation

### Acceptance Criteria

- Agent can execute multiple tool steps.
- Each step is logged.
- Final output includes actions taken and results found.

---

## Milestone 9: LLM Integration

### Objective

Connect the workbench to an LLM API.

### Supported Providers

Initial support may include one of:

- OpenAI API
- Ollama
- LM Studio

### Features

- Send user goal to model.
- Request structured JSON output.
- Allow model to choose tools.
- Validate model output.
- Require approval before dangerous actions such as file writing.

### Concepts Practiced

- LLM API usage
- Structured outputs
- Tool calling
- Guardrails
- Model response validation

### Acceptance Criteria

- LLM can create a plan.
- LLM can request tool execution.
- Tool execution is validated before running.
- Dangerous operations require confirmation.

---

## Milestone 10: Repo Review Agent

### Objective

Build the final capstone feature.

### Command

```bash
workbench review ./repo
```

### Output

The review command should generate:

```text
reports/
  repo-review.json
  repo-review.md
```

### Report Sections

- Repository summary
- File tree overview
- Detected languages/frameworks
- TODO/FIXME findings
- Large files
- Potential risk areas
- Suggested refactor tasks
- Suggested test coverage improvements
- Final recommendation

### Concepts Practiced

- End-to-end application design
- Agentic orchestration
- File analysis
- Structured reporting
- LLM-assisted reasoning
- Tool-based automation

### Acceptance Criteria

- User can review any local repo.
- Output is generated in both Markdown and JSON.
- Report includes actionable recommendations.
- The process is repeatable and logged.

---

## 5. Suggested Folder Structure

```text
python-agentic-workbench/
  README.md
  pyproject.toml
  .env.example
  .gitignore

  workbench/
    __init__.py
    cli.py

    core/
      config.py
      logging.py
      errors.py

    models/
      task.py
      project.py
      report.py
      tool.py

    services/
      task_service.py
      project_service.py
      scan_service.py
      report_service.py

    stores/
      json_store.py

    tools/
      __init__.py
      registry.py
      file_tools.py
      search_tools.py
      api_tools.py
      report_tools.py

    agent/
      planner.py
      executor.py
      memory.py
      loop.py

    integrations/
      llm_client.py
      openai_client.py
      ollama_client.py

  tests/
    test_task_service.py
    test_json_store.py
    test_scan_service.py
    test_tool_registry.py
    test_agent_loop.py

  reports/
    .gitkeep
```

---

## 6. Development Rules

- Keep each module small.
- Avoid global mutable state.
- Use type hints.
- Validate external input.
- Never hardcode secrets.
- Log important execution steps.
- Write tests after each milestone.
- Prefer boring, readable Python over clever abstractions.

---

## 7. Recommended Build Order

1. Build JSON task manager.
2. Refactor into models/services/stores.
3. Add real CLI.
4. Add file scanner.
5. Add Markdown and JSON reports.
6. Add API client.
7. Add async execution.
8. Add tool registry.
9. Add non-LLM agent loop.
10. Add LLM integration.
11. Build final repo review agent.

---

## 8. Success Definition

This project is successful when the developer can:

- Build and run a Python CLI tool confidently.
- Read and write structured files.
- Design Python modules cleanly.
- Use Python for automation.
- Build API clients.
- Use async Python when useful.
- Understand how tool-based agent systems work.
- Integrate an LLM without treating it as magic.
- Debug the system using logs, tests, and structured reports.

---

## 9. Stretch Goals

After completing the core project, optional improvements include:

- Web UI using FastAPI
- SQLite storage
- Plugin-based tools
- Repo memory system
- Vector search over files
- GitHub repository review
- Pull request review mode
- Docker support
- CI pipeline
- HTML report dashboard
- Multi-agent reviewer system
