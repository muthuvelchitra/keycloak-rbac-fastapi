from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str

    ALGORITHM: str = "RS256"

    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()