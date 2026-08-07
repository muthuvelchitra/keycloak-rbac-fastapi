from fastapi import APIRouter, Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/dashboard", response_model=ApiResponse)
def admin_dashboard(user=Depends(require_role("admin"))):
    return ApiResponse(
        success=True,
        message="Admin dashboard fetched successfully",
        data={
            "username": user["preferred_username"],
            "role": "admin"
        }
    )


@router.get("/users", response_model=ApiResponse)
def get_users(user=Depends(require_role("admin"))):
    return ApiResponse(
        success=True,
        message="Users fetched successfully",
        data=[
            "admin_user",
            "manager_user",
            "employee_user",
            "hr_user"
        ]
    )