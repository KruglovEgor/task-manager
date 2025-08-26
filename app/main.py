import os
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.tasks import router as tasks_router
from app.database.connection import engine
from app.database.models import Base

load_dotenv()

app_name = os.getenv("APP_NAME", "Task Manager")
app_version = os.getenv("APP_VERSION", "1.0.0")
debug = os.getenv("DEBUG", "False").lower() == "true"

app = FastAPI(
    title=app_name,
    version=app_version,
    description="API для управления задачами с CRUD операциями",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=debug,
)

cors_origins = os.getenv("CORS_ORIGINS", "[]")
if cors_origins != "[]":
    try:
        origins = eval(cors_origins)
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    except Exception:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

if os.getenv("DEBUG", "False").lower() == "true":
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")

app.include_router(tasks_router, prefix="/api/v1")


@app.get("/", tags=["root"])
def read_root() -> Dict[str, str]:
    return {
        "message": "Task Manager API",
        "version": app_version,
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["health"])
def health_check() -> Dict[str, str]:
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if not debug else "debug",
    )
