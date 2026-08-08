from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer

from jose import JWTError
from jose import jwt

from app.config import settings
from app.core.logger import logger
from app.keycloak import public_key


# ============================================================
# BEARER SECURITY
# ============================================================

security = HTTPBearer(
    auto_error=True
)


# ============================================================
# CURRENT USER
# ============================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.ALGORITHM],
            options={
                "verify_aud": False
            }
        )

        username = payload.get(
            "preferred_username",
            "unknown"
        )

        logger.info(
            "Authentication successful | User: %s",
            username
        )

        return payload

    except JWTError as exc:

        logger.warning(
            "Authentication failed | %s",
            exc
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )