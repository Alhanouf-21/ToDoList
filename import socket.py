import socket
import multiprocessing

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.lock = multiprocessing.Lock()

    def add_task(self, task):
        with self.lock:
            self.tasks.append({"task": task, "priority": None, "due_date": None, "done": False})

    def view_tasks(self):
        if not self.tasks:
            return "No tasks available."
        else:
            result = "Your To-Do List:\n"
            for i, task in enumerate(self.tasks, 1):
                status = "Done" if task["done"] else "Not Done"
                priority = f"Priority: {task['priority']}" if task["priority"] else "No Priority"
                due_date = f"Due Date: {task['due_date']}" if task["due_date"] else "No Due Date"
                result += f"{i}. {task['task']} ({status}) - {priority}, {due_date}\n"
            return result

    def mark_done(self, index):
        if 1 <= index <= len(self.tasks):
            with self.lock:
                self.tasks[index - 1]["done"] = True
            return f"Task '{self.tasks[index - 1]['task']}' marked as done!"
        else:
            return "Invalid task number."

class TaskServer:
    def __init__(self):
        self.task_manager = TaskManager()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 12345

    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server started. Listening for connections...")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Accepted connection from {client_address}")

            client_process = multiprocessing.Process(target=self.handle_client, args=(client_socket,))
            client_process.start()

    def handle_client(self, client_socket):
        while True:
            request = client_socket.recv(1024).decode().strip()

            if not request:
                break

            if request == "1":
                task = client_socket.recv(1024).decode().strip()
                self.task_manager.add_task(task)
                response = f"Task '{task}' added successfully!"
                client_socket.send(response.encode())
            elif request == "2":
                response = self.task_manager.view_tasks()
                client_socket.send(response.encode())
            elif request == "3":
                index = int(client_socket.recv(1024).decode().strip())
                response = self.task_manager.mark_done(index)
                client_socket.send(response.encode())
            else:
                response = "Invalid choice. Please enter a number between 1 and 3."
                client_socket.send(response.encode())

        client_socket.close()

class TaskClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 12345

    def connect(self):
        self.client_socket.connect((self.host, self.port))

    def add_task(self, task):
        self.client_socket.sendall("1".encode())
        self.client_socket.sendall(task.encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def view_tasks(self):
        self.client_socket.sendall("2".encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def mark_done(self, index):
        self.client_socket.sendall("3".encode())
        self.client_socket.sendall(str(index).encode())
        response = self.client_socket.recv(1024).decode()
        print(response)

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    server = TaskServer()
    server_process = multiprocessing.Process(target=server.start)
    server_process.start()

    client = TaskClient()
    client.connect()

    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Mark as Done\n4. Quit")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            task = input("Enter a new task: ")
            client.add_task(task)
        elif choice == "2":
            client.view_tasks()
        elif choice == "3":
            index = int(input("Enter the number of the task to mark as done: "))
            client.mark_done(index)
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    client.close()