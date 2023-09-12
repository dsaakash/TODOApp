import sqlite3

# Create a connection to the database or create it if it doesn't exist
conn = sqlite3.connect('todo.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT NOT NULL
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

def create_task():
    task = input("Enter the task to create : ")
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    conn.commit()
    conn.close()

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

def main():
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
            print("Thanks for to do application!")
            break

if __name__ == "__main__":
    main()
