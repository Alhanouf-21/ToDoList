import socket
import sys
from datetime import datetime
from textblob import TextBlob

tasks = []

def add_task(task):
    # Spell check the task
    spell = TextBlob(task)
    corrected_task = str(spell.correct())

    tasks.append({"task": corrected_task, "priority": None, "due_date": None, "done": False})
    return "Task added successfully!"

def mark_done(index):
    if 1 <= index <= len(tasks):
        tasks[index - 1]["done"] = True
        return f"Task '{tasks[index - 1]['task']}' marked as done!"
    else:
        return "Invalid task number."

def set_priority(index, priority):
    if 1 <= index <= len(tasks):
        tasks[index - 1]["priority"] = priority
        return f"Priority set for task '{tasks[index - 1]['task']}'!"
    else:
        return "Invalid task number."

def set_due_date(index, due_date_str):
    if 1 <= index <= len(tasks):
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        tasks[index - 1]["due_date"] = due_date
        return f"Due date set for task '{tasks[index - 1]['task']}'!"
    else:
        return "Invalid task number."

def view_tasks():
    if not tasks:
        return "No tasks available."
    else:
        tasks_info = []
        for i, task in enumerate(tasks, 1):
            status = "Done" if task["done"] else "Not Done"
            priority = f"Priority: {task['priority']}" if task["priority"] else "No Priority"
            due_date = f"Due Date: {task['due_date']}" if task["due_date"] else "No Due Date"
            tasks_info.append(f"{i}. {task['task']} ({status}) - {priority}, {due_date}")
        return "\n".join(tasks_info)

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode()
        if not request:
            print("Client disconnected.")
            break
        
        if request.startswith("ADD_TASK"):
            task = request.split(":")[1]
            response = add_task(task)
        elif request.startswith("MARK_DONE"):
            index = int(request.split(":")[1])
            response = mark_done(index)
        elif request.startswith("SET_PRIORITY"):
            index, priority = request.split(":")[1:]
            index = int(index)
            response = set_priority(index, priority.capitalize())
        elif request.startswith("SET_DUE_DATE"):
            index, due_date_str = request.split(":")[1:]
            index = int(index)
            response = set_due_date(index, due_date_str)
        elif request == "VIEW_TASKS":
            response = view_tasks()
        elif request == "QUIT":
            print("Client requested to quit.")
            break
        else:
            response = "Invalid request."

        client_socket.send(response.encode())

    client_socket.close()
    sys.exit()

def main(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server is listening on {host}:{port}...")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} has been established!")
        handle_client(client_socket)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python server.py <host> <port>")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        main(host, port)