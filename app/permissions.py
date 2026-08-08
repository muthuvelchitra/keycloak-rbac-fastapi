from fastapi import Depends

from app.dependencies import get_current_user
from app.exceptions.custom_exceptions import ForbiddenException


def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        roles = user.get("realm_access", {}).get("roles", [])

        if required_role not in roles:
            raise ForbiddenException(
                f"'{required_role}' role required to access this resource."
            )

        return user

    return role_checker