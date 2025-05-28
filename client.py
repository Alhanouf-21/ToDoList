import socket
import sys

def main(server_host, server_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Mark as Done\n4. Set Priority\n5. Set Due Date\n6. Quit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            task = input("Enter a new task: ")
            client_socket.send(f"ADD_TASK:{task}".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == '2':
            client_socket.send("VIEW_TASKS".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == '3':
            index = input("Enter the number of the task to mark as done: ")
            client_socket.send(f"MARK_DONE:{index}".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == '4':
            index = input("Enter the number of the task to set priority: ")
            priority = input("Enter priority (High, Medium, Low): ")
            client_socket.send(f"SET_PRIORITY:{index}:{priority}".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == '5':
            index = input("Enter the number of the task to set due date: ")
            due_date = input("Enter due date (YYYY-MM-DD): ")
            client_socket.send(f"SET_DUE_DATE:{index}:{due_date}".encode())
            response = client_socket.recv(1024).decode()
            print(response)
        elif choice == '6':
            client_socket.send("QUIT".encode())
            print("Exiting the to-do list program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

    client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client.py <server_host> <server_port>")
    else:
        server_host = sys.argv[1]
        server_port = int(sys.argv[2])
        main(server_host, server_port)