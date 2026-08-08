from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from app.auth import public_key
from app.config import settings
from app.core.logger import logger


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.ALGORITHM],
            audience="account",
        )

        username = payload.get("preferred_username", "unknown")

        logger.info(
            "Authentication successful | User: %s",
            username
        )

        return payload

    except JWTError as exc:

        logger.warning(
            "Authentication failed | Invalid or expired token | Error: %s",
            str(exc)
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
        )