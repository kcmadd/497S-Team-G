from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl
from pydantic import BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from cryptography.fernet import Fernet
import httpx
from httpx import AsyncClient

app = FastAPI()


class User(BaseModel):
    username: str
    password: str
    fname: str
    lname: str
    phone: str

#for encrypting strings
key = Fernet.generate_key() #encryption key generator
cipher_suite = Fernet(key)

def encrypt_password(password: str):
    encrypted_pass = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_pass

def decrypt_password(encrypted_pass: str):
    password = cipher_suite.decrypt(encrypted_pass)
    return password

#endpoint for signing up
@app.post('/signup')
async def signup(body: dict = Body(...)):
    encrypted_password = encrypt_password(body["password"])
    data = {'username': body["username"], 'password': body["password"], 'fname': body["fname"], 'lname': body["lname"], 'phone': body["phone"]}

    event = {
        "type": "User_Created",
        "data": data
    }
    
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:5005/events", json=event)

    return event

#endpoint for logging in
@app.get('/login')
def login(body: dict = Body(...)):
    return
