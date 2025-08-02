from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
import time

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_requests: int, window_sec: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_sec = window_sec
        self.clients = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        now = time.time()
        client_ip = request.client.host
        self.clients[client_ip] = [t for t in self.clients[client_ip] if t > now - self.window_sec]

        if len(self.clients[client_ip]) >= self.max_requests:
            raise HTTPException(status_code=429, detail="Too Many Requests")

        self.clients[client_ip].append(now)
        response = await call_next(request)
        return response