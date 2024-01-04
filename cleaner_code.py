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

def user_not_found_message():
  #message to display if the user is not found
  window5 = Toplevel()
  Label(window5,text='User not found').pack()
  Button(window5,text='Ok',command=window5.destroy).pack()

def wrong_password_message():
  #message to display if the password is wrong
  window6 = Toplevel()
  Label(window6,text='Wrong password').pack()
  Button(window6,text='Ok',command=window6.destroy).pack()

def login():
  window2 = Toplevel()
  window2.geometry('300x200')
  window2.title('Login')
  
  Label(window2,text='Username').pack()
  username = Entry(window2)
  username.pack()
  
  Label(window2,text='Password').pack()
  password = Entry(window2)
  password.pack()
  
  def try_login():
    user_entered = username.get()
    if not repeat_username(user_entered):
      user_not_found_message()
      return
    
    password_entered = password.get()
    if not verify(user_entered, password_entered):
      wrong_password_message()
      return
    else:
      window2.destroy()
      start_window = Toplevel()
      start_window.geometry('500x300')  
      start_window.title('Guess the artist or song')  
      Button(start_window,text="Play Game",command=play_game).pack()
      Button(start_window,text="stats",command=stats).pack()
      Button(start_window,text='Close',command=start_window.destroy).pack()
  Button(window2,text='Login',command=try_login).pack()

user_filepath = 'users.txt'
special_keys = "!@#$%^&*()_+[]:;'\|,./<>?`~-="

def generate_password():
  #generate a random password
  global password
  password = ''.join(secrets.choice(string.ascii_letters + string.digits + special_keys) for x in range(10))
  #need to show to user so they know it
  password_message(password)
  return password


def password_message(password):
  #message to display the password
  window4 = Toplevel()
  Label(window4,text='Your password is ' + password + '/nWrite it down to remember').pack()
  Button(window4,text='Ok',command=window4.destroy).pack()

#for security reasons, we need to hash the password
def hash_password(password):
  #hash the password
  hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
  return hashed

def save_user(entered_username,password):
  hashed = hash_password(password)
  #saves user information in the text file
  with open(user_filepath,'a') as file:
    file.write(f"{entered_username} {hashed}\n")
  login()



def repeat_username(username):
  #checking if the username is already in the database
  try:
    with open(user_filepath,'r') as file:
      for line in file:
        breaking = line.split()
        if breaking[0] == username:
          #username already exists
          username_exists_message()
          return True
  except FileNotFoundError as error:
    print(error)
  return False


def verify(username,password):
   #check if the username and password are correct from the database
  with open(user_filepath,'r') as file:
    for line in file:
      breaking = line.split()
      if breaking[0] == username:
        hashed_password = breaking[1]
        if hashed_password == hash_password(password):
          #correct password
          return True
        else:
          return False
  return False
        
def username_saving():
  global username_entry
  global entered_username
  entered_username = username_entry.get()   
  if repeat_username(entered_username):
    return      
  else:
    return entered_username

def register():
    window_register = Toplevel()
    window_register.geometry('300x200')
    window_register.title('Register')
    Label(window_register,text='Username').pack()
    #need to enter the username in with enter to store it
    global username_entry
    username_entry = Entry(window_register)
    username_entry.pack()
    Button(window_register,text='Enter',command=username_saving).pack()
    Label(window_register,text='Password').pack()
    Button(window_register,text='Generate Password',command=generate_password).pack()
    Button(window_register,text="continue",command=lambda:[save_user(entered_username,password)]).pack()

def username_exists_message():
  #message to display if the username already exists
  window3 = Toplevel()
  Label(window3,text='Username already exists')
  Button(window3,text='Ok',command=window3.destroy).pack()

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