from fastapi import Depends

from app.dependencies import get_current_user
from app.exceptions.custom_exceptions import ForbiddenException
from app.core.logger import logger


def require_role(required_role: str):

    def role_checker(
        user=Depends(get_current_user)
    ):

        username = user.get(
            "preferred_username",
            "unknown"
        )

        roles = user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )

        logger.info(
            "Role check | User: %s | Required role: %s | User roles: %s",
            username,
            required_role,
            roles
        )

        if required_role not in roles:

            logger.warning(
                "Access denied | User: %s | Required role: %s",
                username,
                required_role
            )

            raise ForbiddenException(
                f"'{required_role}' role required to access this resource."
            )

        logger.info(
            "Authorization successful | User: %s | Role: %s",
            username,
            required_role
        )

        return user

    return role_checker