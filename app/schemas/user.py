from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class UserCreate(BaseModel):

    keycloak_id: str

    username: str

    email: EmailStr | None = None

    full_name: str | None = None

    role: str | None = None


class UserResponse(BaseModel):

    id: int

    keycloak_id: str

    username: str

    email: str | None = None

    full_name: str | None = None

    role: str | None = None

    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )