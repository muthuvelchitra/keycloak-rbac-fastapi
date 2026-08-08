from fastapi import APIRouter
from fastapi import Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse


router = APIRouter(
    prefix="/hr",
    tags=["HR"]
)


@router.get(
    "/dashboard",
    response_model=ApiResponse
)
def hr_dashboard(
    user=Depends(
        require_role("hr")
    )
):

    return ApiResponse(
        success=True,

        message="HR Dashboard fetched successfully",

        data={
            "username": user.get(
                "preferred_username"
            ),

            "role": "hr"
        }
    )


@router.get(
    "/employees",
    response_model=ApiResponse
)
def employee_list(
    user=Depends(
        require_role("hr")
    )
):

    return ApiResponse(
        success=True,

        message="Employee list fetched successfully",

        data=[
            {
                "id": 1,
                "name": "Employee 1",
                "role": "employee"
            },
            {
                "id": 2,
                "name": "Employee 2",
                "role": "employee"
            },
            {
                "id": 3,
                "name": "Employee 3",
                "role": "employee"
            }
        ]
    )