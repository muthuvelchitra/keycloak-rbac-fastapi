from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User

from app.permissions import require_any_role

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ============================================================
# GET ALL USERS
# ADMIN + HR + MANAGER
# ============================================================

@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(

    _: dict = Depends(
        require_any_role(
            "admin",
            "hr",
            "manager"
        )
    ),

    db: Session = Depends(get_db)
):

    return (
        db.query(User)
        .order_by(User.id)
        .all()
    )


# ============================================================
# CREATE USER
# ADMIN + HR
# ============================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def create_user(

    user: UserCreate,

    _: dict = Depends(
        require_any_role(
            "admin",
            "hr"
        )
    ),

    db: Session = Depends(get_db)
):

    existing_username = (
        db.query(User)
        .filter(
            User.username == user.username
        )
        .first()
    )

    if existing_username:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    existing_keycloak_id = (
        db.query(User)
        .filter(
            User.keycloak_id == user.keycloak_id
        )
        .first()
    )

    if existing_keycloak_id:

        raise HTTPException(
            status_code=400,
            detail="Keycloak ID already exists"
        )


    new_user = User(
        **user.model_dump()
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user


# ============================================================
# GET ONE USER
# ADMIN + HR + MANAGER
# ============================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(

    user_id: int,

    _: dict = Depends(
        require_any_role(
            "admin",
            "hr",
            "manager"
        )
    ),

    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


# ============================================================
# DELETE USER
# ADMIN ONLY
# ============================================================

@router.delete(
    "/{user_id}"
)
def delete_user(

    user_id: int,

    _: dict = Depends(
        require_any_role("admin")
    ),

    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(
            User.id == user_id
        )
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted successfully",
        "user_id": user_id
    }