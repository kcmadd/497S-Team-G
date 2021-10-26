from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from cryptography.fernet import Fernet

app = FastAPI()
users = []
user_map = {} #for user lookup

#for encrypting strings
key = Fernet.generate_key() #encryption key generator
cipher_suite = Fernet(key)

def encrypt_password(password: str):
    encrypted_pass = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_pass

def decrypt_password(encrypted_pass: str):
    password = cipher_suite.decrypt(encrypted_pass)
    return password

#temporary place holder for user's account page
#will print to terminal
def account(username: str):
    print('\n\n'+'\033[96mwelcome '+ username) #welcome statment to user
    print('\033[91m'+'username: '+username+'\033[0m')#print username
    print('\033[91m'+'encrypted password: '+user_map[username].decode("utf-8")+'\033[0m')#print encrypted password
    print('\033[91m'+'password: '+decrypt_password(user_map[username]).decode("utf-8")+'\033[0m'+'\n\n')#print decryption of encrypted password
    return

#endpoint for signing up
@app.post('/signup')
def signup(username: str=Body(...), password: str=Body(...)):
    encrypted_password = encrypt_password(password)
    if(username in user_map.keys()):
        print("\n\033[91mUser already taken\033[0m\n")
    else:
        users.append({'username': username, 'encrypted_password': encrypted_password})
        user_map[username] = encrypted_password
        account(username)
    return users

#endpoint for logging in
@app.get('/login')
def login(username: str=Body(...), password: str=Body(...)):
    if(username in user_map.keys()):
        if(password == decrypt_password(user_map[username]).decode("utf-8")):
            account(username)
            #print("password correct")
        else:
            print("\n\033[91mpassword incorrect\033[0m\n")

    else:
        print("\n\033[91mUser does not exist\033[0m\n")

#Tempory endpoint to view all user accounts until we get a DB
@app.get('/userdata')
def get_users():
    return users
