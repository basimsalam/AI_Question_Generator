# app/main.py
from fastapi import FastAPI
from app.routes import router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Question Paper Generator",
    description="Generate exam papers using AI based on curriculum.",
    version="1.0.0"
)

app.include_router(router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
