from typing import Optional 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import requests

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
def get_info(postId : str):
    if postId in idToOwnerInfo:
        return idToOwnerInfo[postId]['details']
    else:
        return JSONResponse(status_code=404, content={"message" : "Post Doesnot Exist in the database."})

@app.post('/posts/{postId}', status_code=200)
async def send_info(postId: str, subletterInfo : user):
    json_userInfo = jsonable_encoder(subletterInfo)
    json_userInfo["postId"] = postId
    if postId in idToOwnerInfo:
        data = json_userInfo
        event = {
            'type': 'Mark_Interested',
            'data': data
        }
        await requests.post("http://localhost:5005/events", event)
        messages[idToOwnerInfo[postId]['user_id']] = json_userInfo   #Pass the user info.
        return data
    else:
        return JSONResponse(status_code=404, content={"message" : "Could not notify the owner since the post doesnot exist."})

@app.post('/posts/{postId}/NoLongerInterested', status_code=200)
async def mark_not_interested(postId: str, userId: user_id):
    json_userInfo = jsonable_encoder(userId)
    json_userInfo["postId"] = postId
    event = {
        'type': 'Mark_Not_Interested',
        'data': json_userInfo
    }
    await requests.post("http://localhost:5005/events", event)
    return "Marked Not Interested."



