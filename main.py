import sqlite3
import datetime
from plyer import notification
import time
import threading

# Create a connection to the database or create it if it doesn't exist
conn = sqlite3.connect('todo.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL,
        reminder_time TEXT
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def create_task():
    task = input("Enter the task to create: ")
    reminder_time = input("Enter the reminder time (HH:MM): ")

    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task, reminder_time) VALUES (?, ?)', (task, reminder_time))
    conn.commit()
    conn.close()

    print(f"Task added to the to-do list with a reminder at {reminder_time}.")

def read_tasks():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def update_task(task_id, new_task):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    
    
def check_reminders():
    while True:
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        now = datetime.datetime.now().strftime('%H:%M')

        # Fetch tasks with reminders
        cursor.execute('SELECT * FROM tasks WHERE reminder_time = ?', (now,))
        tasks = cursor.fetchall()
        conn.close()

        if tasks:
            for task in tasks:
                notification_title = "Task Reminder"
                notification_message = task[1]
                notification_timeout = 10  # Notification duration in seconds
                notification.notify(
                    title=notification_title,
                    message=notification_message,
                    timeout=notification_timeout
                )

        # Sleep for a while before checking again (e.g., every minute)
        time.sleep(60)

def main():
    
    reminder_thread = threading.Thread(target=check_reminders)
    reminder_thread.daemon = True  # This allows the thread to exit when the main program exits
    reminder_thread.start()
    while True:
        print("\nTo-Do List Menu:")
        print("1. Add a task")
        print("2. View tasks")
        print("3. Update a task")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_task()
            print("Task added to the to-do list.")
            check_reminders()
            
        elif choice == "2":
            tasks = read_tasks()
            print("\nTo-Do List:")
            for task in tasks:
                print(f"{task[0]}. {task[1]}")

        elif choice == "3":
            task_id = int(input("Enter the task number to update: "))
            new_task = input("Enter the new task: ")
            update_task(task_id, new_task)
            print("Task updated.")

        elif choice == "4":
            task_id = int(input("Enter the task number to delete: "))
            delete_task(task_id)
            print("Task deleted.")

        elif choice == "5":
            print("Thanks for using the application!")
            break

if __name__ == "__main__":
    main()
