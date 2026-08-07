from fastapi import APIRouter, Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/employee",
    tags=["Employee"]
)


@router.get("/dashboard", response_model=ApiResponse)
def employee_dashboard(user=Depends(require_role("employee"))):
    return ApiResponse(
        success=True,
        message="Employee dashboard fetched successfully",
        data={
            "username": user["preferred_username"],
            "role": "employee"
        }
    )


@router.get("/profile", response_model=ApiResponse)
def employee_profile(user=Depends(require_role("employee"))):
    return ApiResponse(
        success=True,
        message="Employee profile fetched successfully",
        data={
            "username": user["preferred_username"],
            "email": user.get("email"),
            "role": "employee"
        }
    )