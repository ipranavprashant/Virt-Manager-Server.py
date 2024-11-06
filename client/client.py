import socket
import threading
import time

# Send a single request to a server
def send_request(server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 8080))  # Connect to the server's IP and port
    client.send(b"GET / HTTP/1.1\r\n")
    response = client.recv(4096)
    print(response.decode())
    client.close()

# Client thread to send requests to multiple servers
def client_thread(servers):
    for server in servers:
        send_request(server)

# Main function to start the client
if __name__ == "__main__":
    servers = ['192.168.122.101', '192.168.122.102']  # Replace with your VM IPs
    while True:
        client_thread(servers)  # Send requests continuously
        time.sleep(1)  # Wait for 1 second before sending the next round of requests
