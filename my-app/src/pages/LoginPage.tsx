import { useState } from "react";
import keycloak from "../services/keycloak";

function LoginPage() {
  const [loading, setLoading] = useState(false);

  const handleLogin = async () => {
    try {
      setLoading(true);

      await keycloak.login({
  redirectUri: "http://localhost:5173/",
});
    } catch (error) {
      console.error("Login failed:", error);
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <h1>RBAC Keycloak Project</h1>

      <p>Role Based Access Control</p>

      <button onClick={handleLogin} disabled={loading}>
        {loading ? "Redirecting..." : "Login with Keycloak"}
      </button>
    </div>
  );
}

export default LoginPage;