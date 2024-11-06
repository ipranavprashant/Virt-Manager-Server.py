import socket
import threading
import time

# Handle incoming client requests
def handle_request(client_socket):
    # Simulate a CPU-intensive task (e.g., computation)
    time.sleep(1)  # Simulate delay
    client_socket.send(b'HTTP/1.1 200 OK\n\nHello from the server!')
    client_socket.close()

# Server thread to listen for connections and handle requests
def server_thread(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"Server listening on port {port}...")
    while True:
        client_socket, _ = server.accept()
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    server_thread(8080)  # Run the server on port 8080
