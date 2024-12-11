task_list = []

def add_task(task):
    task_list.append(task)
    return task
    

def remove_task(task):
    if task in task_list:
        r = task_list.remove(task)
        return task
    else:
        print("Task not found")

def view_tasks():
    print(task_list)

def duplicate_task(task):
    if task in task_list:
        return "Task already exists"
    else:
        return add_task(task)
    

def main():
    while True:
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View Tasks")
        print("4. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            task = input("Enter task: ")
            duplicate_task(task)
        elif choice == "2":
            task = input("Enter task: ")
            remove_task(task)
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()