# https://medium.com/@mycodingmantras/designing-a-login-register-and-user-authentication-script-in-python-326a11821504


# Step 1:
# Create a login system

import secrets
import string
import hashlib
from getpass import getpass
from datetime import date

from tkinter import Toplevel, Label, Button, Entry, Tk
import tkinter as tkinter

import sqlite3

user_id = None
# connect to the database
conn = sqlite3.connect("fresher.db")
cursor = conn.cursor()
cursor.execute(
    """
  CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT,
    date DATE
  )
"""
)
conn.commit()


def user_not_found_message():
    # message to display if the user is not found
    window5 = Toplevel()
    print("User not found")
    Label(window5, text="User not found").pack()
    Button(window5, text="Ok", command=window5.destroy).pack()


def wrong_password_message():
    # message to display if the password is wrong
    window6 = Toplevel()
    print("Wrong password")
    Label(window6, text="Wrong password").pack()
    Button(window6, text="Ok", command=window6.destroy).pack()


def login(client):
    window2 = Toplevel()
    window2.geometry("300x200")
    window2.title("Login")

    Label(window2, text="Username").pack()
    username = Entry(window2)
    username.pack()

    Label(window2, text="Password").pack()
    password = Entry(window2)
    password.pack()

    def try_login():
        user_entered = username.get()
        # To do: check the username is in the database (optional as it's done implicitly in verify() function)
        # if not is_repeat_username(user_entered): 
        #     user_not_found_message()
        #     return None

        password_entered = password.get()
        global user_id
        user_id = verify(user_entered, password_entered)
        print(user_id)
        if user_id is None:
            wrong_password_message()
            return None
        else:
            window2.destroy()
            # login successful
            #send message to server to say login was succesful
            client.send("LOGIN_SUCCESSFUL")
            

        
            

    Button(window2, text="Login", command=try_login).pack()
    
    


user_filepath = "users.txt"
special_keys = "!@#$%^&*()_+[]:;'\\|,./<>?`~-="


def generate_password():
    # generate a random password
    global password
    password = "".join(
        secrets.choice(string.ascii_letters + string.digits + special_keys)
        for x in range(10)
    )
    # need to show to user so they know it
    password_message(password)
    return password


def password_message(password):
    # message to display the password
    window4 = Toplevel()
    print("Your password is " + password)
    Label(
        window4, text="Your password is " + password + "\nWrite it down to remember"
    ).pack()
    Button(window4, text="Ok", command=window4.destroy).pack()


# for security reasons, we need to hash the password
def hash_password(password):
    # hash the password
    hashed = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hashed


def save_user(entered_username, password, client):
    hashed = hash_password(password)
    # save the username and password to the database
    try:
        current_date = date.today()
        cursor.execute(
            "INSERT INTO users (username, password, date) VALUES (?,?,?)",
            (entered_username, hashed, current_date),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        username_exists_message()
    else:
        login(client)


def is_repeat_username(username):
    # checking if the username is already in the database
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone() is not None:
        # Username already exists
        username_exists_message()
        return True
    return False


def verify(username, password):
    # check if the username and password are correct from the database
    cursor.execute("SELECT password, user_id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    print(result)
    if result is not None:
        hashed_password = result[0]
        if hashed_password == hash_password(password):
            # Correct password
            return result[1]
    return None


def username_saving():
    global username_entry
    global entered_username
    entered_username = username_entry.get()
    if is_repeat_username(entered_username):
        return
    else:
        return entered_username


def register(client):
    window_register = Toplevel()
    window_register.geometry("300x200")
    window_register.title("Register")
    Label(window_register, text="Username").pack()
    # need to enter the username in with enter to store it
    global username_entry
    username_entry = Entry(window_register)
    username_entry.pack()
    Button(window_register, text="Enter", command=username_saving).pack()
    Label(window_register, text="Password").pack()
    Button(window_register, text="Generate Password", command=generate_password).pack()
    Button(
        window_register,
        text="continue",
        command=lambda: [save_user(entered_username, password, client)],
    ).pack()


def username_exists_message():
    # message to display if the username already exists
    window3 = Toplevel()
    Label(window3, text="Username already exists").pack()
    Button(window3, text="Ok", command=window3.destroy).pack()


def login_register(client):
    window = Toplevel()
    window.geometry("300x200")
    window.title("Login or register")
    Button(window, text="Login", command=lambda: login(client)).pack()
    Button(window, text="Register", command=lambda: register(client)).pack()
    Button(window, text="Exit", command=window.destroy).pack()


if __name__ == "__main__":
    from client_code import GameClient
    client = GameClient()

    app = Tk()
    app.geometry("300x200")
    app.title("Music Quiz ?")
    Button(app, text="Login", command=lambda: login_register(client)).pack()
    Button(app, text="Exit", command=app.destroy).pack()
    app.mainloop()
