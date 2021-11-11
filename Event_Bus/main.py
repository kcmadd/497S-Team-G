import json
from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
import random
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
import requests
from httpx import AsyncClient
import httpx


app = FastAPI()
client = AsyncClient()

class Post(BaseModel):
    amenities: str
    num_rooms_available: int
    price: float
    restrictions: str
    lease_duration: str 
    street_address: str
    city: str
    state: str
    country: str # look into converting the location fields to json in the BaseModel

class Data(BaseModel):
    pid: str
    posting: Post

class Event(BaseModel):
    type: str
    data: Data

@app.post('/events', status_code=200)
def event_bus(event: Event):
    print(jsonable_encoder(event))
    # print(await event.json())
    #e = await event.json()
    httpx.post("http://localhost:5000/events", json=jsonable_encoder(event))
    #requests.post("http://localhost:5000/events", json=jsonable_encoder(event))
    # requests.post("http://localhost:5001/events", event)
    # requests.post("http://localhost:5002/events", event)
    # requests.post("http://localhost:5003/events", event)
    # requests.post("http://localhost:5004/events", event)
    return JSONResponse(status_code = 200, content={"message":"event created successfully"})