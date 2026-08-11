import keycloak from "../services/keycloak";
import { useEffect, useState } from "react";
import { getUsers } from "../services/api";

interface User {
  id?: number | string;
  keycloak_id?: string;
  username?: string;
  email?: string;
  full_name?: string;
  role?: string;
}

function EmployeeDashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const data = await getUsers();

        const currentUsername =
          keycloak.tokenParsed?.preferred_username;

        const currentUser = data.find(
          (item: User) =>
            item.username === currentUsername
        );

        setUser(currentUser || null);
      } catch (error) {
        console.error("Failed to load user:", error);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Employee Dashboard</h1>

      <p>
        Welcome,{" "}
        <strong>
          {keycloak.tokenParsed?.preferred_username}
        </strong>
      </p>

      <p>
        Role: <strong>Employee</strong>
      </p>

      <button onClick={() => keycloak.logout()}>
        Logout
      </button>

      <hr />

      <h2>My Profile</h2>

      {loading && <p>Loading profile...</p>}

      {!loading && !user && (
        <p>User information not found.</p>
      )}

      {!loading && user && (
        <table
          border={1}
          cellPadding={10}
          style={{
            borderCollapse: "collapse",
            marginTop: "20px",
          }}
        >
          <tbody>
            <tr>
              <th>Username</th>
              <td>{user.username ?? "-"}</td>
            </tr>

            <tr>
              <th>Email</th>
              <td>{user.email ?? "-"}</td>
            </tr>

            <tr>
              <th>Name</th>
              <td>{user.full_name ?? "-"}</td>
            </tr>

            <tr>
              <th>Role</th>
              <td>{user.role ?? "-"}</td>
            </tr>
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EmployeeDashboard;