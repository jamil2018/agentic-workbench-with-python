from workbench.services.task_service import add_task, list_tasks, complete_task, delete_task

def app() -> None:
    print("Welcome to the Workbench CLI")
    print("-" * 20)
    while True:
        print("-" * 20)
        print("Options:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Quit")
        print("-" * 20)
        choice = input("Enter your choice: ")
        if choice == "1":
            title = input("Enter task title: ")
            result = add_task(title)
            print(f"Task {result['id']} added")
        elif choice == "2":
            tasks = list_tasks()
            print("-" * 20)
            print("Tasks:")
            print("-" * 20)
            if len(tasks) == 0:
                print("No tasks found")
            else:
                for task in tasks:
                    print(f"{task['id']}. {task['title']} {'[DONE]' if task['completed'] else ''}")
            print("-" * 20)
        elif choice == "3":
            task_id = int(input("Enter task ID: "))
            result = complete_task(task_id)
            print(f"Task {result['id']} completed")
        elif choice == "4":
            task_id = int(input("Enter task ID: "))
            deleted_task_id = delete_task(task_id)
            print(f"Task {deleted_task_id} deleted")
        elif choice == "5":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    app()