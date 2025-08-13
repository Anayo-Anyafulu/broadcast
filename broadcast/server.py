import socket
import threading

class BroadcastServer:
    def __init__(self, host='127.0.0.1', port=5555):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.clients = []
        
    def broadcast(self, message, sender=None):
        for client in self.clients:
            if client != sender:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)
    
    def handle_client(self, client):
        while True:
            try:
                message = client.recv(1024)
                if message:
                    self.broadcast(message, client)
                else:
                    self.clients.remove(client)
                    break
            except:
                self.clients.remove(client)
                break
    
    def start(self):
        print("Server is running...")
        while True:
            client, address = self.server.accept()
            print(f"Connected with {address}")
            self.clients.append(client)
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = BroadcastServer()
    server.start()
