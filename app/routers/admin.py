from fastapi import APIRouter
from fastapi import Depends

from app.permissions import require_role
from app.schemas.response import ApiResponse


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get(
    "/dashboard",
    response_model=ApiResponse
)
def admin_dashboard(
    user=Depends(
        require_role("admin")
    )
):

    return ApiResponse(
        success=True,

        message="Welcome to Admin Dashboard",

        data={
            "username": user.get(
                "preferred_username"
            ),

            "role": "admin"
        }
    )


@router.get(
    "/profile",
    response_model=ApiResponse
)
def admin_profile(
    user=Depends(
        require_role("admin")
    )
):

    return ApiResponse(
        success=True,

        message="Admin profile",

        data={

            "username": user.get(
                "preferred_username"
            ),

            "email": user.get(
                "email"
            ),

            "roles": user.get(
                "realm_access",
                {}
            ).get(
                "roles",
                []
            )
        }
    )