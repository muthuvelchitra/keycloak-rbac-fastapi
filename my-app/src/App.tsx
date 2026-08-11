import { useEffect, useState } from "react";
import keycloak from "./services/keycloak";

import LoginPage from "./pages/LoginPage";
import AdminDashboard from "./pages/AdminDashboard";
import HRDashboard from "./pages/HRDashboard";
import ManagerDashboard from "./pages/ManagerDashboard";
import EmployeeDashboard from "./pages/EmployeeDashboard";

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [role, setRole] = useState<string | null>(null);

  useEffect(() => {
    const initKeycloak = async () => {
      try {
        const auth = await keycloak.init({
          onLoad: "check-sso",
          pkceMethod: "S256",
          checkLoginIframe: false,
        });

        setAuthenticated(auth);

        if (auth) {
          const roles = keycloak.tokenParsed?.realm_access?.roles || [];

          console.log("Keycloak Roles:", roles);

          if (roles.includes("admin")) {
            setRole("admin");
          } else if (roles.includes("hr")) {
            setRole("hr");
          } else if (roles.includes("manager")) {
            setRole("manager");
          } else if (roles.includes("employee")) {
            setRole("employee");
          }
        }
      } catch (error) {
        console.error("Keycloak initialization failed:", error);
      } finally {
        setLoading(false);
      }
    };

    initKeycloak();
  }, []);

  if (loading) {
    return (
      <div>
        <h2>Loading...</h2>
      </div>
    );
  }

  if (!authenticated) {
    return <LoginPage />;
  }

  switch (role) {
    case "admin":
      return <AdminDashboard />;

    case "hr":
      return <HRDashboard />;

    case "manager":
      return <ManagerDashboard />;

    case "employee":
      return <EmployeeDashboard />;

    default:
      return (
        <div>
          <h2>No Role Assigned</h2>

          <p>
            Your Keycloak account is authenticated, but no supported role
            is assigned.
          </p>

          <button onClick={() => keycloak.logout()}>
            Logout
          </button>
        </div>
      );
  }
}

export default App;