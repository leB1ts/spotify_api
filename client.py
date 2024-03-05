import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 6942))
client.send("This is a test\n".encode())
from_server = client.recv(4096)
client.close()
print(from_server.decode())
