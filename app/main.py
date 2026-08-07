from fastapi import FastAPI
from fastapi import FastAPI, Depends

from app.auth import keycloak_openid
from app.dependencies import get_current_user
from app.routers import admin, manager, employee, hr

app = FastAPI(
    title="Keycloak RBAC Project",
    version="1.0.0"
)


@app.get("/", tags=["Home"])
def home():
    return {
        "message": "Keycloak RBAC Project is Running"
    }


@app.post("/login", tags=["Authentication"])
def login(username: str, password: str):
    return keycloak_openid.token(
        username=username,
        password=password,
    )


@app.get("/profile", tags=["Authentication"])
def profile(user=Depends(get_current_user)):
    return user


app.include_router(admin.router)
app.include_router(manager.router)
app.include_router(employee.router)
app.include_router(hr.router)