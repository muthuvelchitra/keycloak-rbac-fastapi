import { useEffect, useState } from "react";
import DashboardLayout from "../components/DashboardLayout";
import { getUsers, deleteUser } from "../services/api";

interface User {
  id?: number | string;
  keycloak_id?: string;
  username?: string;
  email?: string;
  full_name?: string;
  role?: string;
}

function AdminDashboard() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [deletingId, setDeletingId] = useState<
    number | string | null
  >(null);

  // ==================================================
  // LOAD USERS
  // ==================================================

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getUsers();

      console.log("Users from backend:", data);

      setUsers(data);
    } catch (err) {
      console.error("Failed to load users:", err);
      setError("Unable to load users from backend.");
    } finally {
      setLoading(false);
    }
  };

  // ==================================================
  // INITIAL LOAD
  // ==================================================

  useEffect(() => {
    loadUsers();
  }, []);

  // ==================================================
  // DELETE USER
  // ==================================================

  const handleDelete = async (user: User) => {
    if (!user.id) {
      alert("User ID not available.");
      return;
    }

    // Protect admin account
    if (user.role === "admin") {
      alert("Admin user cannot be deleted.");
      return;
    }

    const confirmed = window.confirm(
      `Are you sure you want to delete ${
        user.username ?? "this user"
      }?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeletingId(user.id);

      await deleteUser(Number(user.id));

      // Remove deleted user from screen
      setUsers((currentUsers) =>
        currentUsers.filter(
          (currentUser) => currentUser.id !== user.id
        )
      );

      alert("User deleted successfully.");
    } catch (err) {
      console.error("Delete user failed:", err);
      alert("Unable to delete user.");
    } finally {
      setDeletingId(null);
    }
  };

  // ==================================================
  // ROLE COUNTS
  // ==================================================

  const totalUsers = users.length;

  const adminCount = users.filter(
    (user) => user.role === "admin"
  ).length;

  const hrCount = users.filter(
    (user) => user.role === "hr"
  ).length;

  const managerCount = users.filter(
    (user) => user.role === "manager"
  ).length;

  const employeeCount = users.filter(
    (user) => user.role === "employee"
  ).length;

  // ==================================================
  // UI
  // ==================================================

  return (
    <DashboardLayout
      title="Admin Dashboard"
      role="admin"
    >
      {/* ==============================================
          WELCOME SECTION
      ============================================== */}

      <div className="welcome-section">
        <h2>Welcome, Admin</h2>

        <p>
          Manage users, roles and access permissions from
          this dashboard.
        </p>
      </div>

      {/* ==============================================
          STATISTICS CARDS
      ============================================== */}

      <div className="dashboard-cards">

        {/* Total Users */}

        <div className="dashboard-card">
          <h3>Total Users</h3>

          <div className="card-number">
            {totalUsers}
          </div>
        </div>

        {/* Admins */}

        <div className="dashboard-card">
          <h3>Admins</h3>

          <div className="card-number">
            {adminCount}
          </div>
        </div>

        {/* HR */}

        <div className="dashboard-card">
          <h3>HR</h3>

          <div className="card-number">
            {hrCount}
          </div>
        </div>

        {/* Managers */}

        <div className="dashboard-card">
          <h3>Managers</h3>

          <div className="card-number">
            {managerCount}
          </div>
        </div>

        {/* Employees */}

        <div className="dashboard-card">
          <h3>Employees</h3>

          <div className="card-number">
            {employeeCount}
          </div>
        </div>

      </div>

      {/* ==============================================
          USER MANAGEMENT
      ============================================== */}

      <div className="user-management">

        {/* Section Header */}

        <div className="user-management-header">

          <div>
            <h2>User Management</h2>

            <p>
              Manage all registered users and their roles.
            </p>
          </div>

          <button
            className="refresh-btn"
            onClick={loadUsers}
            disabled={loading}
          >
            {loading
              ? "Loading..."
              : "Refresh Users"}
          </button>

        </div>

        {/* ============================================
            LOADING
        ============================================ */}

        {loading && (
          <p>Loading users...</p>
        )}

        {/* ============================================
            ERROR
        ============================================ */}

        {error && (
          <div>
            <p
              style={{
                color: "#dc2626",
                marginBottom: "10px",
              }}
            >
              {error}
            </p>

            <button
              className="refresh-btn"
              onClick={loadUsers}
            >
              Try Again
            </button>
          </div>
        )}

        {/* ============================================
            NO USERS
        ============================================ */}

        {!loading &&
          !error &&
          users.length === 0 && (
            <p>No users found.</p>
          )}

        {/* ============================================
            USERS TABLE
        ============================================ */}

        {!loading &&
          !error &&
          users.length > 0 && (

            <div className="dashboard-table-wrapper">

              <table className="dashboard-table">

                {/* TABLE HEADER */}

                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Action</th>
                  </tr>
                </thead>

                {/* TABLE BODY */}

                <tbody>

                  {users.map((user, index) => (

                    <tr
                      key={
                        user.id ??
                        user.keycloak_id ??
                        index
                      }
                    >

                      {/* ID */}

                      <td>
                        {user.id ?? "-"}
                      </td>

                      {/* USERNAME */}

                      <td>
                        <strong>
                          {user.username ?? "-"}
                        </strong>
                      </td>

                      {/* EMAIL */}

                      <td>
                        {user.email ?? "-"}
                      </td>

                      {/* NAME */}

                      <td>
                        {user.full_name ?? "-"}
                      </td>

                      {/* ROLE */}

                      <td>
                        <span
                          className={`role-badge role-${
                            user.role ?? "unknown"
                          }`}
                        >
                          {user.role ?? "-"}
                        </span>
                      </td>

                      {/* ACTION */}

                      <td>

                        {user.role === "admin" ? (

                          <button
                            className="protected-btn"
                            disabled
                          >
                            Protected
                          </button>

                        ) : (

                          <button
                            className="delete-btn"
                            onClick={() =>
                              handleDelete(user)
                            }
                            disabled={
                              deletingId === user.id
                            }
                          >
                            {deletingId === user.id
                              ? "Deleting..."
                              : "Delete"}
                          </button>

                        )}

                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          )}

      </div>

    </DashboardLayout>
  );
}

export default AdminDashboard;