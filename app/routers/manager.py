from fastapi import APIRouter
from fastapi import Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse


router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)


@router.get(
    "/dashboard",
    response_model=ApiResponse
)
def manager_dashboard(
    user=Depends(
        require_role("manager")
    )
):

    return ApiResponse(
        success=True,

        message="Manager Dashboard fetched successfully",

        data={
            "username": user.get(
                "preferred_username"
            ),

            "role": "manager"
        }
    )


@router.get(
    "/team",
    response_model=ApiResponse
)
def get_team(
    user=Depends(
        require_role("manager")
    )
):

    return ApiResponse(
        success=True,

        message="Manager team fetched successfully",

        data=[
            {
                "name": "Employee 1",
                "role": "employee"
            },
            {
                "name": "Employee 2",
                "role": "employee"
            },
            {
                "name": "Employee 3",
                "role": "employee"
            }
        ]
    )