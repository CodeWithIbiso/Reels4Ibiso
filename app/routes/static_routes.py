from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import HTMLResponse
from typing import List
from pydantic import BaseModel
import os
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()

class Reel(BaseModel):
    id: int
    title: str
    created_time: str
    url: str
    thumbnail: str

def load_template(content: str, title: str = "Reel Manager", extra_scripts: str = "") -> str:
    with open("static/base_template.html", "r") as file:
        template = file.read()
    return (template
            .replace("{{ content }}", content)
            .replace("{{ title }}", title)
            .replace("{{ extra_scripts }}", extra_scripts))

@router.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard():
    with open(os.path.join("static", "dashboard.html"), "r") as file:
        content = file.read()
    
    extra_scripts = """
    <script src="static/components/uploadedReels.js?v=1.0.1"></script>
    <script src="static/components/uploadReel.js?v=1.0.3"></script>
    <script src="static/components/notUploadedReels.js?v=1.0.1"></script>
    <script src="static/components/editReels.js?v=1.0.1"></script>
    <script src="static/components/dragDropUpload.js?v=1.0.0"></script>
    """
    
    if os.getenv("ENV") != "production":
        extra_scripts += '<script src="http://localhost:5500/livereload.js"></script>'
    
    return load_template(content, title="Dashboard - Reel Manager", extra_scripts=extra_scripts)

# security starts
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def fake_decode_token(token):
    # This function should verify the token and return the user information
    return {"sub": "user"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

# security ends

# reels start
from utils.reels import get_reels

@router.get("/reels", response_model=List[Reel])
async def get_all_reels(current_user: dict = Depends(get_current_user)):
    reels = get_reels()
    return reels

# reels end
