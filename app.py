from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
import string, random

app = FastAPI()
url_mapping = {}  # In-memory key-value store

def generate_short_id(num_chars=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=num_chars))

@app.post("/shorten")
async def shorten_url(request: Request):
    data = await request.json()
    long_url = data.get("url")
    if not long_url:
        raise HTTPException(status_code=400, detail="URL is required.")
    
    short_id = generate_short_id()
    url_mapping[short_id] = long_url
    return {"short_url": f"http://localhost:8000/{short_id}"}

@app.get("/{short_id}")
async def redirect_url(short_id: str):
    long_url = url_mapping.get(short_id)
    if long_url:
        return RedirectResponse(long_url)
    raise HTTPException(status_code=404, detail="URL not found.")
