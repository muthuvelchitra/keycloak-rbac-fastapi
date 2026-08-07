from fastapi import APIRouter, Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)


@router.get("/dashboard", response_model=ApiResponse)
def manager_dashboard(user=Depends(require_role("manager"))):
    return ApiResponse(
        success=True,
        message="Manager dashboard fetched successfully",
        data={
            "username": user["preferred_username"],
            "role": "manager"
        }
    )


@router.get("/team", response_model=ApiResponse)
def get_team(user=Depends(require_role("manager"))):
    return ApiResponse(
        success=True,
        message="Manager team fetched successfully",
        data=[
            "Employee 1",
            "Employee 2",
            "Employee 3"
        ]
    )