from pymongo import MongoClient
import certifi 
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")


# Connect to MongoDB with SSL Certificate
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Database and collection
db = client["todolist"]
collection = db["datatodo"]

def add_task(task):
    if collection.find_one({"task": task}):
        return "Task already exists in the database."
    result = collection.insert_one({"task": task})
    return f"Task added with ID: {result.inserted_id}"

def remove_task(task):
    """Removes a task from the database."""
    result = collection.delete_one({"task": task})
    if result.deleted_count > 0:
        return "Task removed successfully."
    return "Task not found in the database."

def view_tasks():
    """Fetches and displays all tasks from the database."""
    tasks = collection.find()
    print("To-Do List:")
    for idx, task in enumerate(tasks, start=1):
        print(f"{idx}. {task['task']}")

def main():
    while True:
        print("\n--- To-Do List Manager ---")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. View Tasks")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter task: ")
            print(add_task(task))
        elif choice == "2":
            task = input("Enter task to remove: ")
            print(remove_task(task))
        elif choice == "3":
            view_tasks()
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
