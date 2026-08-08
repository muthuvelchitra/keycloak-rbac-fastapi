from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # ========================================================
    # KEYCLOAK
    # ========================================================

    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM: str
    KEYCLOAK_CLIENT_ID: str

    # ========================================================
    # JWT
    # ========================================================

    SECRET_KEY: str = "change-this-secret"

    ALGORITHM: str = "RS256"

    # ========================================================
    # POSTGRESQL
    # ========================================================

    POSTGRES_HOST: str = "localhost"

    POSTGRES_PORT: int = 5432

    POSTGRES_USER: str = "postgres"

    POSTGRES_PASSWORD: str

    POSTGRES_DB: str = "rbac_db"

    DATABASE_URL: str | None = None

    # ========================================================
    # ENV
    # ========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ========================================================
    # DATABASE URL
    # ========================================================

    @property
    def database_url(self) -> str:

        if self.DATABASE_URL:

            return self.DATABASE_URL

        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )


settings = Settings()