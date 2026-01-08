from fastapi import FastAPI
from .documents.endpoint import router as documents_router

def register_routers(app: FastAPI):
    app.include_router(documents_router)
