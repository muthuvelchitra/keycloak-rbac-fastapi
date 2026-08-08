from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

from pydantic import BaseModel

from app.dependencies import get_current_user
from app.keycloak import keycloak_openid
from app.core.logger import logger


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


# ============================================================
# LOGIN RESPONSE
# ============================================================

class LoginResponse(BaseModel):

    access_token: str

    token_type: str = "bearer"


# ============================================================
# LOGIN
# ============================================================

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    logger.info(
        "Login attempt | User: %s",
        form_data.username
    )

    try:

        token = keycloak_openid.token(
            username=form_data.username,
            password=form_data.password,
            grant_type="password"
        )

        logger.info(
            "Login successful | User: %s",
            form_data.username
        )

        return {
            "access_token": token["access_token"],
            "token_type": "bearer"
        }

    except Exception as exc:

        logger.warning(
            "Login failed | User: %s | %s",
            form_data.username,
            exc
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )


# ============================================================
# CURRENT USER
# ============================================================

@router.get("/me")
def get_current_user_info(
    current_user: dict = Depends(
        get_current_user
    )
):

    return {

        "user_id": current_user.get(
            "sub"
        ),

        "username": current_user.get(
            "preferred_username"
        ),

        "email": current_user.get(
            "email"
        ),

        "full_name": current_user.get(
            "name"
        ),

        "roles": current_user.get(
            "realm_access",
            {}
        ).get(
            "roles",
            []
        )
    }