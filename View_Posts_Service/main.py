from typing import Optional
from fastapi import FastAPI
import hashlib
import random
import base64
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse

app = FastAPI()
posts = []

class Post(BaseModel):
    description: str
    num_rooms: int
    price: float
    location: str

def create_postid():
    random_number = str(hex(random.randint(1000,9999)))
    print(random_number)
    return random_number
 
# For testing and showcasing purpose only. Real function will get data from centralized data source
@app.post('/createpost', status_code = 201)
async def post_info(post: Post):
    id = create_postid()
    posts.append({"pid":id, "posting":post})
    return JSONResponse(status_code = 201, message="Post created successfully")

@app.get('/postings')
def get_posts(post: Post):
    return posts