"""FastAPI Application Entry Point"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import submissions, adops, config_routes
from app.db.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(submissions.router, prefix="/api/submissions", tags=["AM Submissions"])
app.include_router(adops.router, prefix="/api/adops", tags=["Ad Ops Dashboard"])
app.include_router(config_routes.router, prefix="/api/config", tags=["Configuration"])

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION}

# 
