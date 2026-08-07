from fastapi import APIRouter, Depends
from app.permissions import require_role

router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)


@router.get("/dashboard")
def hr_dashboard(user=Depends(require_role("hr"))):
    return {
        "message": "Welcome HR",
        "user": user["preferred_username"],
        "role": "hr"
    }


@router.get("/employees")
def employee_list(user=Depends(require_role("hr"))):
    return {
        "message": "Employee List",
        "requested_by": user["preferred_username"]
    }