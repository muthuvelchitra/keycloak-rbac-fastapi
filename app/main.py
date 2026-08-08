from fastapi import FastAPI, Depends, HTTPException, status

from app.auth import keycloak_openid
from app.dependencies import get_current_user

from app.routers import admin, manager, employee, hr

from app.exceptions.handlers import register_exception_handlers

from app.core.logger import logger


app = FastAPI(
    title="Keycloak RBAC Project",
    version="1.0.0"
)


# Register global exception handlers
register_exception_handlers(app)


# Register routers
app.include_router(admin.router)
app.include_router(manager.router)
app.include_router(employee.router)
app.include_router(hr.router)


logger.info("Keycloak RBAC application started")


@app.get("/")
def home():

    logger.info("Home endpoint accessed")

    return {
        "message": "Keycloak RBAC Project is Running"
    }


@app.post("/login")
def login(
    username: str,
    password: str
):

    logger.info(
        "Login attempt | User: %s",
        username
    )

    try:

        token = keycloak_openid.token(
            username=username,
            password=password,
        )

        logger.info(
            "Login successful | User: %s",
            username
        )

        return token

    except Exception as exc:

        logger.warning(
            "Login failed | User: %s | Error: %s",
            username,
            str(exc)
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


@app.get("/profile")
def profile(
    user=Depends(get_current_user)
):

    username = user.get(
        "preferred_username",
        "unknown"
    )

    logger.info(
        "Profile accessed | User: %s",
        username
    )

    return user