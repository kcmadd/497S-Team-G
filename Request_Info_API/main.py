from typing import Optional 
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class user(BaseModel):
    user_name: str
    phone_number: str

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

@app.get('/posts/{postId}')
def get_info(postId : str):
    if postId in idToOwnerInfo:
        return idToOwnerInfo[postId]['details']
    else:
        return JSONResponse(status_code=404, content={"message" : "Post Doesnot Exist in the database."})

@app.post('/posts/{postId}')
def send_info(postId: str, subletterInfo : user):
    json_userInfo = jsonable_encoder(subletterInfo)
    if postId in idToOwnerInfo:
        messages[idToOwnerInfo[postId]['user_id']] = json_userInfo   #Pass the user info.
        return JSONResponse(status_code=200, content={"message" : "Message sent"})
    else:
        return JSONResponse(status_code=404, content={"message" : "Could not notify the owner since the post doesnot exist."})


