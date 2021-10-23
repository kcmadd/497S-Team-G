from typing import Optional 
from fastapi import FastAPI

idToOwnerInfo = {
    'P1' : [1, 'Owner 1', 'XXXXXXXXX'],
    'P2' : [2, 'Owner 2', 'XXXXXXXXX'],
    'P3' : [3, 'Owner 3', 'XXXXXXXXX'],
    'P4' : [4, 'Owner 4', 'XXXXXXXXX'],
    'P5' : [5, 'Owner 5', 'XXXXXXXXX'],
    'P6' : [6, 'Owner 6', 'XXXXXXXXX'],
}  #Stores the mapping of postId to Customer Info. 

messages = {

} #Stores mapping of Owner Id to the message it received.

app = FastAPI()

@app.get('/posts/{postId}')
def get_info(postId : str):
    if postId in idToOwnerInfo:
        return idToOwnerInfo[postId][1:]
    else:
        return "Post Doesnot Exist in the database."

@app.post('/posts/{postId}')
def send_info(userName : str, contactInfo : str):
    if postId in idToOwnerInfo:
        messages[idToOwnerInfo[postId][0]] = [userName, contactInfo, postId]
        return JSONResponse(status_code=200)
    else:
        return JSONResponse(status_code=404, content={"message" : "Could not notify the owner since the post doesnot exist."})


