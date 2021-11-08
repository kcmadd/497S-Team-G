from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
import random
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
import requests

app = FastAPI();

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

class User(BaseModel):
    name: str
    phone_number: str

posts = []
user_info = []

@app.get('/location_filter/{city}', status_code=200)
def filter_by_location(city: str):
    post_by_loc = []
    for i in range(len(posts)):
        post_data = jsonable_encoder(posts[i])
        if post_data["data"]["city"] == city:
            post_by_loc.append(posts[i])
        else:
            raise HTTPException(
            status_code=404,
            detail='No postings for this location available'
        )
    return post_by_loc
    
# this should be under user_info_send
@app.post('/mark_interested', status_code=201)
def mark_interested(post: Post):
    pid = str(random.randint(0,4))
    user_id = str(random.randint(0,4))
    interested_users = []
    interested_users.append(user_id)
    posting = {
        "pid": pid,
        "posting": post, 
        "interested_users": interested_users
    }
    posts.append(posting)
    return JSONResponse(status_code=201, content="The post has been marked interested")

app.post('/events', status_code=200)
def push_event(post: Post):
    sent_post = jsonable_encoder(post)
    if sent_post['type'] == 'Post_Created':
        posts.append(sent_post['data'])
    
    if sent_post['type'] == 'User_Created':
        user_info.append(sent_post['data'])

    if sent_post['type'] == 'Mark_Interested':
        pid = str(random.randint(0,4))
        user_id = str(random.randint(0,4))
        for i in range(len(posts)):
            if posts[i]['pid'] == pid:
                posts[i]['interested_users'].append(user_id)
                break
    
    if sent_post['type'] == 'Mark_Not_Interested':
        pid = str(random.randint(0,4))
        user_id = str(random.randint(0,4))
        for i in range(len(posts)):
            if posts[i]['pid'] == pid:
                del posts[i]['interested_users'][user_id]
                break




