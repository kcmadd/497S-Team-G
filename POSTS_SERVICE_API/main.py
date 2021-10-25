from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, JSONResponse
import random
from fastapi.encoders import jsonable_encoder


class Post(BaseModel):
    description: str
    num_rooms_available: int
    price: float
    location: str
    
app = FastAPI()
# [{pid: str, description: str, num_rooms: int, price: double, location: str},]
posts = []
def create_postid():
    random_number = str(hex(random.randint(1000,9999)))
    print(random_number)
    return random_number
 
@app.post('/createpost', status_code = 201)
async def post_info(post: Post):
    id = create_postid()
    posts.append({"pid":id, "posting":post})
    return JSONResponse(status_code = 201, message="Post created successfully")

@app.get('/viewpost/{postid}')
async def get_post(postid : str):
    for i in range(len(posts)):
        post_json = jsonable_encoder(posts[i])
        if post_json['pid'] == postid:
            post = post_json
        else:
            post=None
            
    if post is None:
        raise HTTPException(
            status_code = 404,
            detail='post does not exist'
        )
    return post