import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import contacts, company, deals, leads, pipelines, activities, analytics,projects, clients, tasks

# -------------------------------------------------
# Create database tables
# -------------------------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------------------------
# Initialize FastAPI
# -------------------------------------------------
app = FastAPI(title="CRM_Project Management")

# -------------------------------------------------
# Frontend URL + Allowed Origins
# -------------------------------------------------
# Used for emails or frontend redirects
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# Multi-origin support (comma separated)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://127.0.0.1:3000"
)

_allowed_origins = [
    origin.strip() for origin in ALLOWED_ORIGINS.split(",") if origin.strip()
]

# Allow all origins if developer explicitly sets "*"
allow_all = "*" in _allowed_origins

# -------------------------------------------------
# CORS Middleware
# -------------------------------------------------
if allow_all:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,  # Cannot use credentials with "*"
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(contacts.router,prefix="/contacts",tags=["contacts"])
app.include_router(company.router,prefix="/companies",tags=["companies"])
app.include_router(deals.router,prefix="/deals",tags=["deals"])
app.include_router(leads.router,prefix="/leads",tags=["leads"])
app.include_router(pipelines.router,prefix="/pipelines",tags=["pipelines"])
app.include_router(activities.router,prefix="/activities",tags=["activities"])
app.include_router(analytics.router,prefix="/analytics",tags=["analytics"])

app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(tasks.router)


# -------------------------------------------------
# Root endpoint
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "message": "Welcome to CRM API",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend_url": FRONTEND_URL,
        "allowed_origins": _allowed_origins
    }
