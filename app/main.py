from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.auth import router as auth_router
from app.core.logger import logger
from app.database import create_users_table, test_database_connection
from app.exceptions.handlers import register_exception_handlers
from app.permissions import router as permissions_router

from app.routers.admin import router as admin_router
from app.routers.employee import router as employee_router
from app.routers.hr import router as hr_router
from app.routers.manager import router as manager_router
from app.routers.users import router as users_router


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="RBAC Keycloak API",
    description="Role Based Access Control API using FastAPI, Keycloak and PostgreSQL",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# EXCEPTION HANDLERS
# ============================================================

register_exception_handlers(app)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(permissions_router)

app.include_router(users_router)

app.include_router(admin_router)
app.include_router(hr_router)
app.include_router(manager_router)
app.include_router(employee_router)


# ============================================================
# FRONTEND
# ============================================================

app.mount(
    "/ui",
    StaticFiles(directory=FRONTEND_DIR, html=True),
    name="frontend",
)


# ============================================================
# STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():

    logger.info("Starting RBAC application")

    # --------------------------------------------------------
    # PostgreSQL connection test
    # --------------------------------------------------------

    if not test_database_connection():

        logger.error("PostgreSQL connection failed")

        raise RuntimeError(
            "Unable to connect to PostgreSQL"
        )

    logger.info(
        "PostgreSQL connection verified"
    )

    # --------------------------------------------------------
    # Create database tables
    # --------------------------------------------------------

    create_users_table()

    logger.info(
        "Application startup complete"
    )


# ============================================================
# HOME
# ============================================================

@app.get(
    "/",
    tags=["Default"]
)
def home():

    return {
        "message": "RBAC Keycloak API is running",
        "frontend": "/ui",
        "swagger": "/docs",
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get(
    "/health",
    tags=["Default"]
)
def health_check():

    return {
        "status": "healthy"
    }