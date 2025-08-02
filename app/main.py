from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

from routes import users, patients, practices, static_routes
from routes.upload import router as upload_router  # Import the upload router
from middleware.rate_limit import RateLimitMiddleware

import os
import threading
from livereload import Server

if os.getenv("ENV") != "production":
    def start_livereload():
        server = Server()
        server.watch("static/")
        server.watch("templates/")
        server.serve(root=".", port=5500)

    threading.Thread(target=start_livereload, daemon=True).start()

app = FastAPI()

# Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(RateLimitMiddleware, max_requests=100, window_sec=60)

# stop caching
class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

app.add_middleware(CacheControlMiddleware)

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Pydantic Model
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# Include Routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(patients.router, prefix="/patients", tags=["Patients"])
app.include_router(practices.router, prefix="/practices", tags=["Practices"])
app.include_router(static_routes.router, tags=["Static"])
app.include_router(upload_router, prefix="/api", tags=["Upload"])  # Include the upload router

# Endpoints
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
