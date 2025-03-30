import time

from fastapi import Request


async def log_middleware(request: Request, call_next):
    """
    Middleware for logging HTTP requests.

    Args:
        request (Request): The incoming HTTP request
        call_next (Callable): The next middleware or route handler

    Returns:
        Response: The HTTP response
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(
        f"{request.method} {request.url} - {response.status_code} ({process_time:.2f}s)"
    )
    return response


__all__ = ["log_middleware"]
