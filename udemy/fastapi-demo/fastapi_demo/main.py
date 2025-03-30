# fastapi_demo/main.py
from fastapi import FastAPI

from fastapi_demo.items import item_router
from fastapi_demo.middlewares import log_middleware

app = FastAPI(
    title="Item Manager",
    description="A FastAPI demo project showcasing CRUD operations on items.\n* Create, read, update, and delete items\n * Async operations\n * Request logging\n * Input validation\n\n This API currently doesn't require authentication.",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# middleware
app.middleware("http")(log_middleware)

# routers
app.include_router(item_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    print("====== Started Item Manager ======")
