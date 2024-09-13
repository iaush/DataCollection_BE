from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
from collections import defaultdict
from typing import Dict


class RateLimitter(BaseHTTPMiddleware):

    def __init__(self, app: FastAPI, max_requests: int, time_window: float):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window
        self.rate_limit_records = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        self.rate_limit_records[client_ip] = [
            timestamp for timestamp in self.rate_limit_records[client_ip]
            if current_time - timestamp < self.time_window
        ]

        if len(self.rate_limit_records[client_ip]) >= self.max_requests:
            return Response("Request Rate limited", status_code=429)

        self.rate_limit_records[client_ip].append(current_time)

        response = await call_next(request)
        return response
    

class CSPHeader(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self'; "
            "img-src 'self';"
        )
        return response