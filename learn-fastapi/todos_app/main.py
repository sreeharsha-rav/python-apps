from fastapi import FastAPI
from todos_app.middleware import LogRequestsMiddleware, configure_logging
from todos_app.models import Base
from todos_app.database import engine
from todos_app.routers import auth, todos

configure_logging()

app = FastAPI(
    title="Todos API",
    description="A simple API to manage todos with validation and error handling.",
    version="1.0.0"
)

app.add_middleware(LogRequestsMiddleware)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
