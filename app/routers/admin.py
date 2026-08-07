from fastapi import APIRouter, Depends

from app.permissions import require_role

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard")
def admin_dashboard(user=Depends(require_role("admin"))):
    return {
        "message": "Welcome Admin",
        "username": user["preferred_username"],
        "role": "admin"
    }


@router.get("/users")
def get_users(user=Depends(require_role("admin"))):
    return {
        "message": "User list fetched successfully",
        "requested_by": user["preferred_username"]
    }