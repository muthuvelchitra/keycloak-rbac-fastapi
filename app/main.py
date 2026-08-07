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


@app.get("/admin")
def admin(user=Depends(get_current_user)):
    roles = user["realm_access"]["roles"]

    if "admin" not in roles:
        return {"detail": "Access Denied"}

    return {
        "message": "Welcome Admin",
        "user": user["preferred_username"]
    }


@app.get("/manager")
def manager(user=Depends(get_current_user)):
    roles = user["realm_access"]["roles"]

    if "manager" not in roles:
        return {"detail": "Access Denied"}

    return {
        "message": "Welcome Manager",
        "user": user["preferred_username"]
    }


@app.get("/employee")
def employee(user=Depends(get_current_user)):
    roles = user["realm_access"]["roles"]

    if "employee" not in roles:
        return {"detail": "Access Denied"}

    return {
        "message": "Welcome Employee",
        "user": user["preferred_username"]
    }


@app.get("/hr")
def hr(user=Depends(get_current_user)):
    roles = user["realm_access"]["roles"]

    if "hr" not in roles:
        return {"detail": "Access Denied"}

    return {
        "message": "Welcome HR",
        "user": user["preferred_username"]
    }