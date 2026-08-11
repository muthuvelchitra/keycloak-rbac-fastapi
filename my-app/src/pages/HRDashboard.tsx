import { useEffect, useState } from "react";
import keycloak from "../services/keycloak";
import { getUsers } from "../services/api";

interface User {
  id?: number | string;
  keycloak_id?: string;
  username?: string;
  email?: string;
  full_name?: string;
  role?: string;
}

function HRDashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await getUsers();
        setUsers(data);
      } catch (err) {
        console.error(err);
        setError("Unable to load users.");
      } finally {
        setLoading(false);
      }
    };

    loadUsers();
  }, []);

  const handleLogout = () => {
    keycloak.logout({
      redirectUri: window.location.origin,
    });
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>HR Dashboard</h1>

      <p>
        Welcome,{" "}
        <strong>
          {keycloak.tokenParsed?.preferred_username}
        </strong>
      </p>

      <p>
        Role: <strong>HR</strong>
      </p>

      <button onClick={handleLogout}>
        Logout
      </button>

      <hr />

      <h2>Employees</h2>

      {loading && <p>Loading users...</p>}

      {error && (
        <p style={{ color: "red" }}>
          {error}
        </p>
      )}

      {!loading && !error && (
        <table
          border={1}
          cellPadding={10}
          style={{
            borderCollapse: "collapse",
            width: "100%",
            marginTop: "20px",
          }}
        >
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Name</th>
              <th>Role</th>
            </tr>
          </thead>

          <tbody>
            {users.map((user, index) => (
              <tr key={user.id ?? user.keycloak_id ?? index}>
                <td>{user.username ?? "-"}</td>
                <td>{user.email ?? "-"}</td>
                <td>{user.full_name ?? "-"}</td>
                <td>{user.role ?? "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default HRDashboard;