from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from app.dependencies import get_current_user


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"]
)


# ============================================================
# REQUIRE ONE ROLE
# ============================================================

def require_role(required_role: str):

    def role_checker(
        current_user: dict = Depends(get_current_user)
    ):

        roles = current_user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )

        if required_role not in roles:

            raise HTTPException(
                status_code=403,
                detail=f"{required_role} role required"
            )

        return current_user

    return role_checker


# ============================================================
# REQUIRE ANY ROLE
# ============================================================

def require_any_role(*required_roles: str):

    def role_checker(
        current_user: dict = Depends(get_current_user)
    ):

        user_roles = set(
            current_user.get(
                "realm_access",
                {}
            ).get(
                "roles",
                []
            )
        )

        if not user_roles.intersection(
            required_roles
        ):

            raise HTTPException(
                status_code=403,
                detail=(
                    "One of these roles is required: "
                    + ", ".join(required_roles)
                )
            )

        return current_user

    return role_checker


# ============================================================
# CHECK AUTHENTICATION
# ============================================================

@router.get("/check")
def check_permission(
    current_user: dict = Depends(get_current_user)
):

    return {
        "message": "Authentication successful",

        "username": current_user.get(
            "preferred_username"
        ),

        "roles": current_user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )
    }


# ============================================================
# ADMIN
# ============================================================

@router.get("/admin")
def admin_permission(
    current_user: dict = Depends(
        require_role("admin")
    )
):

    return {
        "message": "Admin access granted",

        "username": current_user.get(
            "preferred_username"
        ),

        "roles": current_user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )
    }


# ============================================================
# HR
# ============================================================

@router.get("/hr")
def hr_permission(
    current_user: dict = Depends(
        require_role("hr")
    )
):

    return {
        "message": "HR access granted",

        "username": current_user.get(
            "preferred_username"
        )
    }


# ============================================================
# MANAGER
# ============================================================

@router.get("/manager")
def manager_permission(
    current_user: dict = Depends(
        require_role("manager")
    )
):

    return {
        "message": "Manager access granted",

        "username": current_user.get(
            "preferred_username"
        )
    }


# ============================================================
# EMPLOYEE
# ============================================================

@router.get("/employee")
def employee_permission(
    current_user: dict = Depends(
        require_role("employee")
    )
):

    return {
        "message": "Employee access granted",

        "username": current_user.get(
            "preferred_username"
        )
    }