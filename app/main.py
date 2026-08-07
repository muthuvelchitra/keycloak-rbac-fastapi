from fastapi import FastAPI
from app.auth import keycloak_openid

app = FastAPI(title="Keycloak RBAC Project")


@app.get("/")
def home():
    return {"message": "Keycloak RBAC Project is Running"}


@app.post("/login")
def login(username: str, password: str):
    token = keycloak_openid.token(
        username=username,
        password=password,
    )

    return token