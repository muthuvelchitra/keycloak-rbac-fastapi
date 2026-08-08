from keycloak import KeycloakOpenID

from app.config import settings
from app.core.logger import logger


# ============================================================
# KEYCLOAK CONNECTION
# ============================================================

logger.info(
    "Initializing Keycloak connection"
)


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
)


logger.info(
    "Keycloak initialized successfully | Realm: %s",
    settings.KEYCLOAK_REALM
)


# ============================================================
# LOAD PUBLIC KEY
# ============================================================

def load_public_key():

    key = keycloak_openid.public_key()

    if not key:

        raise RuntimeError(
            "Keycloak public key is empty"
        )

    # Add PEM header if necessary

    if "BEGIN PUBLIC KEY" not in key:

        key = (
            "-----BEGIN PUBLIC KEY-----\n"
            + key
            + "\n-----END PUBLIC KEY-----"
        )

    logger.info(
        "Keycloak public key loaded successfully"
    )

    return key


# ============================================================
# PUBLIC KEY
# ============================================================

public_key = load_public_key()