import socket

class RPIClient:
    def __init__(self, server_ip, port=65432):
        self.server_ip = server_ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect(self):
        """Establishes a connection to the server (robot)."""
        try:
            self.sock.connect((self.server_ip, self.port))
            print(f"Connected to {self.server_ip}:{self.port}")
        except Exception as e:
            print(f"Failed to connect: {e}")
    
    def send_message(self, message):
        """Sends a message to the server (robot)."""
        try:
            self.sock.sendall(message.encode('utf-8'))
            print(f"Sent: {message}")
        except Exception as e:
            print(f"Failed to send message: {e}")
    
    def receive_message(self):
        """Waits indefinitely for and receives messages from the server (robot)."""
        try:
            while True:  # Infinite loop to wait indefinitely for messages
                data = self.sock.recv(1024)  # Buffer size is 1024 bytes
                if data:
                    print(f"Received: {data.decode('utf-8')}")
                    return data.decode('utf-8')
                else:
                    print("No data received. Connection might be closed.")
                    break
        except Exception as e:
            print(f"Failed to receive message: {e}")
    
    def close(self):
        """Closes the connection."""
        self.sock.close()
        print("Connection closed")

# Example usage
if __name__ == "__main__":
    client = RPIClient('192.168.2.1')  # Robot IP address
    client.connect()
    client.send_message("prof_morozov")  # Send location name as message
    response = client.receive_message()  # Wait indefinitely for robot's message
    print(f"Robot Response: {response}")
    client.close()
