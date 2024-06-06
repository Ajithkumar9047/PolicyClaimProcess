from fastapi import Request, HTTPException
from collections import defaultdict
import time

rate_limit_store = defaultdict(list)

class RateLimitMiddleware:
    def __init__(self, app, max_requests: int, window_seconds: int):
        self.app = app
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            request = Request(scope, receive)
            client_ip = request.client.host
            current_time = time.time()

            request_times = rate_limit_store[client_ip]
            request_times = [t for t in request_times if current_time - t < self.window_seconds]

            if len(request_times) >= self.max_requests:
                response = HTTPException(status_code=429, detail="Rate limit exceeded")
                await response(scope, receive, send)
                return

            request_times.append(current_time)
            rate_limit_store[client_ip] = request_times

        await self.app(scope, receive, send)
