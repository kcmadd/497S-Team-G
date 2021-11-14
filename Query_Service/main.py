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
from pymongo import *
import asyncio
import motor.motor_asyncio
import os

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

class Data(BaseModel):
    pid: str
    posting: Post

class Event(BaseModel):
    type: str
    data: Data

class User(BaseModel):
    name: str
    phone_number: str

#client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://root:example@localhost:27888/?authSource=admin")
username = os.getenv("ME_username")
password = os.getenv("ME_password")
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://root:example@mongo:27017/')
#client = MongoClient("mongodb://root:example@mongo:27017/")

db1 = client.posts
db2 = client.user_info

post_collection = db1.post_collection
user_collection = db2.user_collection

print(post_collection)

async def database(body):
    #post = jsonable_encoder(student)
    print (body)
    if body["type"] == "Post_Created":
        print("insert to db")
        new_post = post_collection.insert_one(body["data"])
        print("finished")
        #created_post = await post_collection.find_one({"_id": new_post.inserted_id})
        return JSONResponse(status_code=200, content={"item": "posted"})
    
    if body["type"] == "User_Created":
        new_user = await user_collection.insert_one(body)
        created_user = user_collection.find_one({"_id": body.inserted_id})
        return JSONResponse(status_code=200, content=created_user)

@app.post("/events", status_code=200)
async def run_ops(body: dict = Body(...)):
    database(body)
    print("finished")

@app.get("/posts", status_code=200)
async def list_posts():
    # posts = await post_collection.find().to_list(10)
    # return posts
    for document in await post_collection.to_list(length=100):
        print(document)

"""
@app.get("/users", status_code=200)
async def list_posts():
    users = await user_collection.find().to_list(10)
    return users

@app.get('/location_filter/{city}', status_code=200)
async def filter_by_location(city: str):
    if city is not None:
        location_posts = await post_collection.find({"data": {"city":city}})
    else:
        raise HTTPException(
        status_code=404,
        detail='No postings for this location available'
    )
    return location_posts
"""

# posts = []
# user_info = []
    
# # this should be under user_info_send
# @app.post('/mark_interested', status_code=201)
# def mark_interested(post: Post):
#     pid = str(random.randint(0,4))
#     user_id = str(random.randint(0,4))
#     interested_users = []
#     interested_users.append(user_id)
#     posting = {
#         "pid": pid,
#         "posting": post, 
#         "interested_users": interested_users
#     }
#     posts.append(posting)
#     return JSONResponse(status_code=201, content="The post has been marked interested")

# app.post('/events', status_code=200)
# def push_event(post: Post):
#     sent_post = jsonable_encoder(post)
#     if sent_post['type'] == 'Post_Created':
#         posts.append(sent_post['data'])
    
#     if sent_post['type'] == 'User_Created':
#         user_info.append(sent_post['data'])

#     if sent_post['type'] == 'Mark_Interested':
#         pid = str(random.randint(0,4))
#         user_id = str(random.randint(0,4))
#         for i in range(len(posts)):
#             if posts[i]['pid'] == pid:
#                 posts[i]['interested_users'].append(user_id)
#                 break
    
#     if sent_post['type'] == 'Mark_Not_Interested':
#         pid = str(random.randint(0,4))
#         user_id = str(random.randint(0,4))
#         for i in range(len(posts)):
#             if posts[i]['pid'] == pid:
#                 del posts[i]['interested_users'][user_id]
#                 break




