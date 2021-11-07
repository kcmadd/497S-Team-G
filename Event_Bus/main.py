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


app = FastAPI()

@app.post('/events', status_code=200)
async def event_bus(event: dict = Body(...)):
    requests.post("http://localhost:5000/events", event)
    requests.post("http://localhost:5001/events", event)
    requests.post("http://localhost:5002/events", event)
    requests.post("http://localhost:5003/events", event)
    requests.post("http://localhost:5004/events", event)
    return JSONResponse(status_code = 200, content="event created successfully")