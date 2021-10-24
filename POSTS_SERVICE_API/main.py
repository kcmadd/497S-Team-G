from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl, BaseModel
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
import random
from fastapi.encoders import jsonable_encoder


class Post(BaseModel):
    #pid: str
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
    print(posts)
    return posts

@app.get('/viewpost/{postid}')
async def get_post(postid : str):
    for i in range(len(posts)):
        post_json = jsonable_encoder(posts[i])
        #posting = [l[postid] for l in posts]
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

    
    
# def create_short_link(original_url: str):
#     to_encode = f'{original_url}'

#     b64_encoded_str = base64.urlsafe_b64encode(
#         hashlib.sha256(to_encode.encode()).digest()).decode()
#     return b64_encoded_str[:7]

# @app.post('/link/shorten')
# def get_short_link(url: HttpUrl = Body(..., embed=True)):
#     short_link = create_short_link(url)
#     links.append({'short_link': short_link, 'original_url': url})
#     return links

# @app.get('/{short_link}')
# def redirect(short_link: str):
#     # obj = db.query(ShortenedUrl).filter_by(short_link = short_link).first()
#     short_links = [l["short_link"] for l in links]
#     original_urls = [l["original_url"] for l in links]
#     for i in range(len(short_links)):
#         if short_links[i] == short_link:
#             obj = {"short_link": short_links[i], "original_url": original_urls[i]}
#             break
#     if obj is None:
#         raise HTTPException(
#             status_code=404,
#             detail='The link does not exist, could not redirect.'
#         )
#     return RedirectResponse(url=obj["original_url"])
