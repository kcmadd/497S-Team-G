from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import requests
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
import random
import httpx
from httpx import AsyncClient
from fastapi.encoders import jsonable_encoder
import json

# posting data content schema
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

app = FastAPI()
client = AsyncClient()

posts = [] # {“pid”: str, “posting” : {“amenities” : str, “num_rooms_availables” : int, “price” : float, “Restrictions”: str  (#ex: no pets, no smoking, couples only), students “lease_duration”: str, “location” : { “street_address” : str “city”: str, “state”: str, “country”: str}}}

def create_postid():
    random_number = str(hex(random.randint(1000,9999)))
    print(random_number)
    return random_number
 
# This endpoint for a sublessor to create a posting for a lease 
@app.post('/createpost', status_code = 201)
async def post_info(post: Post):
    id = create_postid()
    data = {"pid":id, "posting":jsonable_encoder(post)}
    posts.append(data)
    event = {
            "type": "Post_Created",
            "data": data
        }
    
    async with httpx.AsyncClient() as client:
        await client.post("http://localhost:5005/events", json=event)

    return event

# This endpoint to view a particular post based on postid 
@app.get('/viewpost/{postid}', status_code= 200)
async def get_post(postid : str):
    for i in range(len(posts)):
        post_json = jsonable_encoder(posts[i])
        if post_json['pid'] == postid:
            post = post_json
        else:
            post = None
     
    if post is None:
        raise HTTPException(
            status_code = 404,
            detail='post does not exist'
        )
    return post

@app.post('/events', status_code = 200)
async def send_status(event: dict = Body(...)):
    print("Recieved Event", event)
    return {"message": "received"}
    