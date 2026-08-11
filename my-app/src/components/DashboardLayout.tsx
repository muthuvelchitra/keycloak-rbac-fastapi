import React from "react";
import keycloak from "../services/keycloak";

interface DashboardLayoutProps {
  title: string;
  role: string;
  children: React.ReactNode;
}

function DashboardLayout({
  title,
  role,
  children,
}: DashboardLayoutProps) {
  const username =
    keycloak.tokenParsed?.preferred_username || "User";

  const handleLogout = () => {
    keycloak.logout({
      redirectUri: window.location.origin,
    });
  };

  return (
    <div className="dashboard-layout">

      {/* =========================
          SIDEBAR
      ========================== */}

      <aside className="sidebar">

        <div className="sidebar-logo">
          <h2>RBAC</h2>
          <span>Access Control System</span>
        </div>

        <nav>

          <button className="nav-item active">
            Dashboard
          </button>

          {/* ADMIN MENU */}

          {role === "admin" && (
            <>
              <button className="nav-item">
                Users
              </button>

              <button className="nav-item">
                Roles
              </button>

              <button className="nav-item">
                Settings
              </button>
            </>
          )}

          {/* HR MENU */}

          {role === "hr" && (
            <>
              <button className="nav-item">
                Employees
              </button>

              <button className="nav-item">
                Requests
              </button>
            </>
          )}

          {/* MANAGER MENU */}

          {role === "manager" && (
            <>
              <button className="nav-item">
                My Team
              </button>

              <button className="nav-item">
                Requests
              </button>
            </>
          )}

          {/* EMPLOYEE MENU */}

          {role === "employee" && (
            <>
              <button className="nav-item">
                My Profile
              </button>

              <button className="nav-item">
                My Requests
              </button>
            </>
          )}

        </nav>

        {/* Logout */}

        <button
          className="sidebar-logout"
          onClick={handleLogout}
        >
          Logout
        </button>

      </aside>


      {/* =========================
          MAIN CONTENT
      ========================== */}

      <main className="dashboard-main">

        {/* Header */}

        <header className="dashboard-header">

          <div>
            <h1>{title}</h1>

            <p>
              Role Based Access Control System
            </p>
          </div>

          <div className="user-info">

            <strong>
              {username}
            </strong>

            <span>
              {role.toUpperCase()}
            </span>

          </div>

        </header>


        {/* Page Content */}

        <section className="dashboard-content">
          {children}
        </section>

      </main>

    </div>
  );
}

export default DashboardLayout;