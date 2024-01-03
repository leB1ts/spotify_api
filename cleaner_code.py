#https://medium.com/@mycodingmantras/designing-a-login-register-and-user-authentication-script-in-python-326a11821504


# Step 1:
# Create a login system

import secrets
import string
import hashlib
from getpass import getpass

from tkinter import (
  Toplevel,
  Label,
  Button,
  Entry,
  Tk
)
import tkinter as tkinter



def login():
  window2 = Toplevel()
  window2.geometry('300x200')
  window2.title('Login')
  Label(window2,text='Username').pack()
  username = Entry(window2).pack()
  Label(window2,text='Password').pack()
  password = Entry(window2).pack()
  Button(window2,text='Login',command=verfiy).pack()

def verfiy():
   #check if the username and password are correct from the database
   pass

def register():
    pass

def login_register():
  window = Toplevel()
  window.geometry('300x200')
  window.title('Login or register')
  Button(window,text='Login',command = login).pack()
  Button(window,text='Register',command = register).pack()
  Button(window,text='Exit',command=window.destroy).pack()




if __name__ == "__main__":
  app = Tk()
  app.geometry('300x200')
  app.title('Music Quiz ?')
  Button(app,text='Login',command=login_register).pack()
  Button(app,text='Exit',command=app.destroy).pack()
  app.mainloop()