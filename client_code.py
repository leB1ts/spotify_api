#fresh clent code that actually works and runs as intended
import socket
import login_or_register
from tkinter import *

class GameClient:
    def __init__(self, host="localhost", port=6942):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))

    def send(self, data):
        self.client.sendall(data.encode())

    def receive(self):
        try:
            return self.client.recv(4096).decode("utf-8")
        except BlockingIOError:
            return None

if __name__ == "__main__":
    client = GameClient()
    client.client.setblocking(False)  # Set the socket to non-blocking mode
    root = Tk()
    root.withdraw()  # Hide the root window

    def check_for_data():
        data = client.receive()
        if data is not None:
            print(f"Received data: {data}")
            if data == "LOGIN_WINDOW":
                print("Starting login window")
                login_or_register.login_register(client)
            if data == "GAME_WINDOW":
                print("Starting game window")
                # Start the game window
                pass


        root.after(100, check_for_data)  # Check for new data every 100 ms

    check_for_data()
    root.mainloop()
   
  