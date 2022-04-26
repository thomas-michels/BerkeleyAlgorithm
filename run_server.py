import socket
import threading

class ThreadedServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            cur_thread = threading.current_thread()
            print(f"{cur_thread.name}: server listening...")
            client, address = self.sock.accept()
            client.send(b"Iniciando nova thread")
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                cur_thread = threading.current_thread()
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    response = data
                    print(f"{cur_thread.name}: {str(response, encoding='ascii')}")
                    client.send(b"connected")
                else:
                    print("disconnected")
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False

if __name__ == "__main__":
    ThreadedServer('',8000).listen()
