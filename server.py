import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.1', 8080))
serv.listen(5)
print("Server is listening...")
while True:
    conn, addr = serv.accept()
    print(f"Accepted connection from {addr}")
    from_client = ""
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode("utf-8")
        print(f"Received data: {from_client}")
        conn.send("I am SERVER\n".encode())
    conn.close()
    print('client disconnected')