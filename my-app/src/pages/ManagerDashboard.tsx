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

function ManagerDashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const data = await getUsers();
        setUsers(data);
      } catch (error) {
        console.error("Failed to load users:", error);
      } finally {
        setLoading(false);
      }
    };

    loadUsers();
  }, []);

  return (
    <div style={{ padding: "30px" }}>
      <h1>Manager Dashboard</h1>

      <p>
        Welcome,{" "}
        <strong>
          {keycloak.tokenParsed?.preferred_username}
        </strong>
      </p>

      <p>
        Role: <strong>Manager</strong>
      </p>

      <button onClick={() => keycloak.logout()}>
        Logout
      </button>

      <hr />

      <h2>Employees</h2>

      {loading && <p>Loading employees...</p>}

      {!loading && users.length === 0 && (
        <p>No employees found.</p>
      )}

      {!loading && users.length > 0 && (
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
            {users
              .filter((user) => user.role === "employee")
              .map((user, index) => (
                <tr
                  key={
                    user.id ??
                    user.keycloak_id ??
                    index
                  }
                >
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

export default ManagerDashboard;