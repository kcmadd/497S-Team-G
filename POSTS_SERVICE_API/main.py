from typing import Optional
from fastapi import FastAPI
import hashlib
import base64
from pydantic import HttpUrl
from fastapi import FastAPI, Depends, Body, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse

app = FastAPI()
links = [] # [{"sl": x, "ou":x}, ...]
def create_short_link(original_url: str):
    to_encode = f'{original_url}'

    b64_encoded_str = base64.urlsafe_b64encode(
        hashlib.sha256(to_encode.encode()).digest()).decode()
    return b64_encoded_str[:7]

@app.post('/link/shorten')
def get_short_link(url: HttpUrl = Body(..., embed=True)):
    short_link = create_short_link(url)
    links.append({'short_link': short_link, 'original_url': url})
    return links

@app.get('/{short_link}')
def redirect(short_link: str):
    # obj = db.query(ShortenedUrl).filter_by(short_link = short_link).first()
    short_links = [l["short_link"] for l in links]
    original_urls = [l["original_url"] for l in links]
    for i in range(len(short_links)):
        if short_links[i] == short_link:
            obj = {"short_link": short_links[i], "original_url": original_urls[i]}
            break
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail='The link does not exist, could not redirect.'
        )
    return RedirectResponse(url=obj["original_url"])

# Fix mapping for html/json request
mapped_links = []
@app.get('/mapping/json')
def get_mapping():
    short_links = [l["short_link"] for l in links]
    print(short_links)
    original_urls = [l["original_url"] for l in links]
    for i in range(len(short_links)):
        mapped_links.append({"original_url": original_urls[i], "short_link": short_links[i]})
    if not mapped_links:
        raise HTTPException(
            status_code=404,
            detail='No mappings in storage'
        )
    return mapped_links

@app.get('/mapping/html', response_class = HTMLResponse)
def get_mapping():
    mapped_links = []
    short_links = [l["short_link"] for l in links]
    original_urls = [l["original_url"] for l in links]
    for i in range(len(short_links)):
        mapped_links.append({"original_url": original_urls[i], "short_link": short_links[i]})
    if not mapped_links:
        return """
        <html>
            <head>
                <title>LURL -> SURL Mappings</title>
            </head>
            <body>
                <h1>List of Mappings</h1>
                <p> No LURL -> SURL Mapping available</p>
            </body>
        </html>
    """
    html = """
    <html>
        <head>
            <title>LURL -> SURL Mappings</title>
        </head>
        <body>
         <h1>List of Mappings</h1>
        <table border='1'>
        <tr><th>Original LURL</th><th>SURL</th></tr>
            """
    for d in mapped_links:
        html += "<tr>" + "<td>" + d["original_url"] + "</td>" + "<td>" + d["short_link"] + "</td>" + "</tr>"
           
    html += """
            </body>
        </html>
        """
    return html

