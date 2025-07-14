# app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="AI Question Paper Generator",
    description="Generate exam papers using AI based on curriculum.",
    version="1.0.0"
)

app.include_router(router)
