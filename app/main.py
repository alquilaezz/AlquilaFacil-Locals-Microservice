from fastapi import FastAPI
from .database import Base, engine
from .routers import locals, local_categories, comments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Locals Service")

app.include_router(locals.router)
app.include_router(local_categories.router)
app.include_router(comments.router)
