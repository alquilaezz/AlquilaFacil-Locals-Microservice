from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routers import locals, local_categories, comments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Locals Service")

origins = [
    "http://localhost:5173",                # para desarrollo local
    "https://alquilaezz.netlify.app",       # tu front en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 👈 cualquier origen
    allow_credentials=False, # 👈 importante: con "*" no uses credentials
    allow_methods=["*"],     # todos los métodos
    allow_headers=["*"],     # todos los headers
)

app.include_router(locals.router)
app.include_router(local_categories.router)
app.include_router(comments.router)
