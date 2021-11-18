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
import uuid

app = FastAPI()


class User(BaseModel):
    uid: str
    username: str
    password: str
    fname: str
    lname: str
    phone: str

#for encrypting strings
key = b'6AE8AUmjBcDpaoTXKnexCUzKmXbgxZGYfQuAFlNsdTg=' #encryption key generator
cipher_suite = Fernet(key)

def encrypt_password(password: str):
    encrypted_pass = cipher_suite.encrypt(password.encode('utf-8'))
    return encrypted_pass.decode("utf-8")

def decrypt_password(encrypted_pass: str):
    encrypted_pass = encrypted_pass.encode("utf-8")
    password = cipher_suite.decrypt(encrypted_pass).decode("utf-8")
    return password

#endpoint for signing up
@app.post('/signup')
async def signup(body: dict = Body(...)):
    encrypted_password = encrypt_password(body["password"])
    uid = str(uuid.uuid4())
    data = {"user_id": uid, 'username': body["username"], 'password': encrypted_password, 'fname': body["fname"], 'lname': body["lname"], 'phone': body["phone"]}

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

@app.post('/events', status_code = 200)
async def send_status(event: dict = Body(...)):
    print("Recieved Event", event)
    return {"message": "received"}