import json
from datetime import datetime

# File to store tasks
TASKS_FILE = 'tasks.json'

def load_tasks():
    """Load tasks from the JSON file."""
    try:
        with open(TASKS_FILE, 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []
    return tasks

def save_tasks(tasks):
    """Save tasks to the JSON file."""
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

def display_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("\n❌ No tasks available!")
        return
    print("\n📋 Task List:")
    for idx, task in enumerate(tasks, 1):
        print(f"{idx}. {task['title']} - Deadline: {task['deadline']} - {task['status']}")

def add_task(tasks):
    """Add a new task."""
    title = input("\nEnter task title: ")
    description = input("Enter task description: ")
    deadline = input("Enter task deadline (YYYY-MM-DD): ")

    try:
        # Validate deadline format
        deadline = datetime.strptime(deadline, '%Y-%m-%d').date()
    except ValueError:
        print("⚠️ Invalid date format. Please use YYYY-MM-DD.")
        return
    
    task = {
        'title': title,
        'description': description,
        'deadline': str(deadline),
        'status': 'Pending'
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Task '{title}' added!")

def edit_task(tasks):
    """Edit an existing task."""
    display_tasks(tasks)
    try:
        task_num = int(input("\nEnter task number to edit: "))
        task = tasks[task_num - 1]
    except (ValueError, IndexError):
        print("⚠️ Invalid task number!")
        return

    print(f"\nEditing task: {task['title']}")
    task['title'] = input(f"New title (current: {task['title']}): ") or task['title']
    task['description'] = input(f"New description (current: {task['description']}): ") or task['description']
    task['status'] = input(f"New status (current: {task['status']}): ") or task['status']
    
    new_deadline = input(f"New deadline (current: {task['deadline']}): ")
    if new_deadline:
        try:
            task['deadline'] = str(datetime.strptime(new_deadline, '%Y-%m-%d').date())
        except ValueError:
            print("⚠️ Invalid date format. Keeping the current deadline.")
    
    save_tasks(tasks)
    print(f"✅ Task '{task['title']}' updated!")

def delete_task(tasks):
    """Delete a task."""
    display_tasks(tasks)
    try:
        task_num = int(input("\nEnter task number to delete: "))
        task = tasks.pop(task_num - 1)
    except (ValueError, IndexError):
        print("⚠️ Invalid task number!")
        return

    save_tasks(tasks)
    print(f"❌ Task '{task['title']}' deleted!")

def sort_tasks_by_deadline(tasks):
    """Sort tasks by deadline."""
    tasks.sort(key=lambda task: datetime.strptime(task['deadline'], '%Y-%m-%d'))
    print("\n✅ Tasks sorted by deadline!")

def task_manager():
    """Main loop for the task manager app."""
    tasks = load_tasks()

    while True:
        print("\n🔧 Task Manager App")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Sort Tasks by Deadline")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            display_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            edit_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            sort_tasks_by_deadline(tasks)
        elif choice == "6":
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid option, try again.")

if __name__ == "__main__":
    task_manager()
