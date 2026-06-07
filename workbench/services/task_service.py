from pathlib import Path
from workbench.stores.json_store import load_json, save_json

TASKS_FILE = Path("tasks.json")

def add_task(title: str) -> dict:
    tasks = load_json(TASKS_FILE)
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "completed": False,
    }
    tasks.append(task)
    save_json(TASKS_FILE, tasks)
    return task

def list_tasks() -> list[dict]:
    return load_json(TASKS_FILE)

def complete_task(task_id: int) -> dict:
    tasks = load_json(TASKS_FILE)
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["completed"] = True
        save_json(TASKS_FILE, tasks)
    return task

def delete_task(task_id: int) -> None:
    tasks = load_json(TASKS_FILE)
    tasks = [t for t in tasks if t["id"] != task_id]
    save_json(TASKS_FILE, tasks)
    return task_id
    