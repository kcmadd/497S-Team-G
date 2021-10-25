from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()
posts = [] # [{"sl": x, "ou":x}, ...]

@app.get('/postings')
def redirect():
    # obj = db.query(ShortenedUrl).filter_by(short_link = short_link).first()
    if posts is None:
        raise HTTPException(
            status_code=404,
            detail='No postings available'
        )
    return RedirectResponse(url=posts)