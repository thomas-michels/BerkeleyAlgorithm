"""
    Module for run client
"""

from time import sleep
from app.client import Client
from datetime import datetime
import socket

def client(ip, port, message):
    # c = Client()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(bytes(message, 'ascii'))
    try:
        while True:
            response = str(sock.recv(1024), 'ascii')
            print("Received: {}".format(response))
            if response == "get time":
                sock.send(bytes("enviando", 'ascii'))

            elif response == "connected":
                sock.send(bytes(str(datetime.now()), 'ascii'))
            else:
                sock.send(b"teste")
            sleep(1)

    except Exception:
        pass
    
    finally:
        sock.close()

if __name__ == "__main__":
    client("localhost", 8000, "new connection")
