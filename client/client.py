# import socket
# import threading
# import time

# # Send a single request to a server
# def send_request(server_ip):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((server_ip, 8080))  # Connect to the server's IP and port
#     client.send(b"GET / HTTP/1.1\r\n")
#     response = client.recv(4096)
#     print(response.decode())
#     client.close()

# # Client thread to send requests to multiple servers
# def client_thread(servers):
#     for server in servers:
#         send_request(server)

# # Main function to start the client
# if __name__ == "__main__":
#     servers = ['192.168.122.122', '192.168.122.222']  # Replace with your VM IPs
#     while True:
#         client_thread(servers)  # Send requests continuously
#         time.sleep(1)  # Wait for 1 second before sending the next round of requests


import socket
import threading
import time

# Send a single request to a server
def send_request(server_ip):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((server_ip, 8080))  # Connect to the server's IP and port
        # Send a complete HTTP GET request
        client.sendall(b"GET / HTTP/1.1\r\nHost: " + server_ip.encode() + b"\r\n\r\n")
        
        # Receive response from server
        response = client.recv(4096)
        print(f"Response from {server_ip}:\n{response.decode()}")
        
    except Exception as e:
        print(f"Error connecting to {server_ip}: {e}")
    finally:
        client.close()

# Client thread to send requests to a single server
def client_thread(server_ip):
    send_request(server_ip)

# Main function to start the client
if __name__ == "__main__":
    servers = ['192.168.122.116', '192.168.122.222']  # Replace with your VM IPs

    while True:
        threads = []
        
        # Start a thread for each server request
        for server in servers:
            thread = threading.Thread(target=client_thread, args=(server,))
            thread.start()
            threads.append(thread)
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        time.sleep(1)  # Wait for 1 second before sending the next round of requests
