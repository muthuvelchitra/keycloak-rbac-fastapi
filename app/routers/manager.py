from fastapi import APIRouter, Depends
from app.permissions import require_role

router = APIRouter(
    prefix="/manager",
    tags=["Manager"]
)


@router.get("/dashboard")
def manager_dashboard(user=Depends(require_role("manager"))):
    return {
        "message": "Welcome Manager",
        "user": user["preferred_username"],
        "role": "manager"
    }


@router.get("/team")
def get_team(user=Depends(require_role("manager"))):
    return {
        "message": "Manager Team Details",
        "requested_by": user["preferred_username"]
    }