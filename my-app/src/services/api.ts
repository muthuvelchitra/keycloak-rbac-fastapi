import keycloak from "./keycloak";

const API_BASE_URL = "http://127.0.0.1:8000";


// Get all users
export async function getUsers() {
  try {
    // Refresh token if it is close to expiry
    await keycloak.updateToken(30);

    const token = keycloak.token;

    if (!token) {
      throw new Error("Access token not available");
    }

    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Get users failed:", error);
    throw error;
  }
}


// Get individual user
export async function getUser(userId: number) {
  try {
    await keycloak.updateToken(30);

    const token = keycloak.token;

    if (!token) {
      throw new Error("Access token not available");
    }

    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Get user failed:", error);
    throw error;
  }
}


// Create user
export async function createUser(userData: {
  username: string;
  email: string;
  full_name: string;
  role: string;
}) {
  try {
    await keycloak.updateToken(30);

    const token = keycloak.token;

    if (!token) {
      throw new Error("Access token not available");
    }

    const response = await fetch(`${API_BASE_URL}/users/`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(userData),
    });

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Create user failed:", error);
    throw error;
  }
}


// Delete user
export async function deleteUser(userId: number) {
  try {
    await keycloak.updateToken(30);

    const token = keycloak.token;

    if (!token) {
      throw new Error("Access token not available");
    }

    const response = await fetch(`${API_BASE_URL}/users/${userId}`, {
      method: "DELETE",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(
        `API request failed: ${response.status} ${response.statusText}`
      );
    }

    return await response.json();
  } catch (error) {
    console.error("Delete user failed:", error);
    throw error;
  }
}