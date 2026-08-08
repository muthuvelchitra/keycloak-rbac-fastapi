from keycloak import KeycloakOpenID

from app.config import settings
from app.core.logger import logger


logger.info("Initializing Keycloak connection")


keycloak_openid = KeycloakOpenID(
    server_url=settings.KEYCLOAK_SERVER_URL,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    realm_name=settings.KEYCLOAK_REALM,
)


public_key = (
    "-----BEGIN PUBLIC KEY-----\n"
    + keycloak_openid.public_key()
    + "\n-----END PUBLIC KEY-----"
)


logger.info(
    "Keycloak initialized successfully | Realm: %s",
    settings.KEYCLOAK_REALM
)