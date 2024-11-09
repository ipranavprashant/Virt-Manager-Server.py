# import socket
# import threading
# import time

# # Handle incoming client requests
# def handle_request(client_socket):
#     # Simulate a CPU-intensive task (e.g., computation)
#     time.sleep(1)  # Simulate delay
#     client_socket.send(b'HTTP/1.1 200 OK\n\nHello from the server!')
#     client_socket.close()

# # Server thread to listen for connections and handle requests
# def server_thread(port):
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('0.0.0.0', port))
#     server.listen(5)
#     print(f"Server listening on port {port}...")
#     while True:
#         client_socket, _ = server.accept()
#         client_handler = threading.Thread(target=handle_request, args=(client_socket,))
#         client_handler.start()

# if __name__ == "__main__":
#     server_thread(8080)  # Run the server on port 8080



import socket
import threading
import time
import math

def cpu_intensive_task():
    primes = []
    for num in range(1, 10000):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# Handle incoming client requests
def handle_request(client_socket):
    # Perform CPU-intensive task
    cpu_intensive_task()
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
