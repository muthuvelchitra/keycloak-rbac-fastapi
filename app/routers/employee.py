from fastapi import APIRouter, Depends
from app.permissions import require_role

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.get("/dashboard")
def employee_dashboard(user=Depends(require_role("employee"))):
    return {
        "message": "Welcome Employee",
        "user": user["preferred_username"],
        "role": "employee"
    }


@router.get("/profile")
def employee_profile(user=Depends(require_role("employee"))):
    return {
        "message": "Employee Profile",
        "requested_by": user["preferred_username"]
    }