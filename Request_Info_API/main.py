from typing import Optional 
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import requests
import httpx

class user(BaseModel):
    uid: str
    fname: str
    lname: str
    email: str 
    phone: str
    # user_name: str
    # phone_number: str

class user_id(BaseModel):
    uid: str

userInfo = [{
    "user_id": 1,
    "details": {
        "name" : "Owner 1",
        "role": "owner",
        "phone_number": "XXXXXXXXXX"
   }
}, {"user_id": 2,
    "details": {
        "name" : "Owner 2",
        "role": "owner",
        "phone_number": "XXXXXXXXXX"
   }
}, {"user_id": 3,
    "details": {
        "name" : "Owner 3",
        "role": "owner",
        "phone_number": "XXXXXXXXXX"
   }
}]

idToOwnerInfo = {
    'P1' : userInfo[0],
    'P2' : userInfo[1],
    'P3' : userInfo[2]
    # 'P4' : [4, 'Owner 4', 'XXXXXXXXX'],
    # 'P5' : [5, 'Owner 5', 'XXXXXXXXX'],
    # 'P6' : [6, 'Owner 6', 'XXXXXXXXX'],
}  #Stores the mapping of postId to Customer Info. 


messages = {

} #Stores mapping of Owner Id to the message it received.

app = FastAPI()

@app.get('/posts/{postId}', status_code=200)
async def get_info(postId : str):
    #
    json_userInfo = {}
    json_userInfo["postId"] = postId
    data = json_userInfo
    event = {
        'type': 'Get_Owner_Info',
        'data': data
    }
    async with httpx.AsyncClient() as client:
        await client.post("http://event_bus:5005/events", json=event)

    return ""
    #else:
        #return JSONResponse(status_code=404, content={"message" : "Post Doesnot Exist in the database."})

@app.post('/posts/{postId}', status_code=200)
async def send_info(postId: str, subletterInfo : user):
    json_userInfo = jsonable_encoder(subletterInfo)
    json_userInfo["postId"] = postId
    # if postId in idToOwnerInfo:
    data = json_userInfo
    event = {
        'type': 'Mark_Interested',
        'data': data
    }
    async with httpx.AsyncClient() as client:
        await client.post("http://event_bus:5005/events", json=event)
    # messages[idToOwnerInfo[postId]['user_id']] = json_userInfo   #Pass the user info.
    return data
    # else:
    #     return JSONResponse(status_code=404, content={"message" : "Could not notify the owner since the post doesnot exist."})

@app.post('/posts/{postId}/NoLongerInterested', status_code=200)
async def mark_not_interested(postId: str, userId: user_id):
    json_userInfo = jsonable_encoder(userId)
    json_userInfo["postId"] = postId
    event = {
        'type': 'Mark_Not_Interested',
        'data': json_userInfo
    }
    async with httpx.AsyncClient() as client:
            await client.post("http://event_bus:5005/events", json=event)
    return "Marked Not Interested."

@app.post('/events', status_code = 200)
async def send_status(event: dict = Body(...)):
    print("Recieved Event", event)
    return {"message": "received"}

