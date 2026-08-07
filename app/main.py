from fastapi import FastAPI, Depends
from app.auth import keycloak_openid
from app.dependencies import get_current_user

app = FastAPI(title="Keycloak RBAC Project")


@app.get("/")
def home():
    return {"message": "Keycloak RBAC Project is Running"}


@app.post("/login")
def login(username: str, password: str):
    return keycloak_openid.token(
        username=username,
        password=password,
    )


@app.get("/profile")
def profile(user=Depends(get_current_user)):
    return user