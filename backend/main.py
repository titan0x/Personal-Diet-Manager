from config import settings
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware


from models import *

from routers import user_router
from auth import auth_router 

app = FastAPI(
    title=settings.app_name,
    description="API do zarządzania dietą",
    debug=settings.debug,
    version="0.1.0"
)

app.include_router(user_router)


# CORS dla Next.js
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów
app.include_router(auth_router)
app.include_router(user_router)


@app.get("/")
def root():
    return {"message": "Personal Diet Manager API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}

