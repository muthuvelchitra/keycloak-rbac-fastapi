import Keycloak from "keycloak-js";

const keycloak = new Keycloak({
  url: "http://localhost:8080",
  realm: "RBAC-Realm",
  clientId: "rbac-app",
});

export default keycloak;