from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
import random
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

class Post(BaseModel):
    description: str
    num_rooms: int
    price: float
    location: str

class User(BaseModel):
    name: str
    phone_number: str

app = FastAPI()
posts = []
user_info = []

@app.get('/location_filter/{location}')
def filter_by_location(location: str):
    post_by_loc = []
    for i in range(len(posts)):
        post_data = jsonable_encoder(posts[i])
        if post_data["data"]["location"] == location:
            post_by_loc.append(posts[i])
        else:
            raise HTTPException(
            status_code=404,
            detail='No postings for this location available'
        )
    return post_by_loc

@app.post('/mark_interested', status_code=201)
async def mark_interested(post: Post):
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
    return JSONResponse(status_code=201, message="The post has been marked interested")


@app.get('/')
def redirect():
    # obj = db.query(ShortenedUrl).filter_by(short_link = short_link).first()
    if posts is None:
        raise HTTPException(
            status_code=404,
            detail='No postings available'
        )
    return RedirectResponse(url=posts)