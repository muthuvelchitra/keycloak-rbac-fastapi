const tokenKey = "rbac_access_token";


const loginView =
    document.getElementById("loginView");

const dashboardView =
    document.getElementById("dashboardView");

const loginForm =
    document.getElementById("loginForm");

const loginMessage =
    document.getElementById("loginMessage");

const profileBox =
    document.getElementById("profile");

const resultBox =
    document.getElementById("result");

const actions =
    document.getElementById("actions");

const welcome =
    document.getElementById("welcome");


// ============================================================
// TOKEN
// ============================================================

function getToken() {

    return localStorage.getItem(
        tokenKey
    );
}


function setToken(token) {

    localStorage.setItem(
        tokenKey,
        token
    );
}


function clearToken() {

    localStorage.removeItem(
        tokenKey
    );
}


// ============================================================
// API
// ============================================================

async function api(
    path,
    options = {}
) {

    const headers =
        new Headers(
            options.headers || {}
        );


    const token = getToken();


    if (token) {

        headers.set(
            "Authorization",
            `Bearer ${token}`
        );

    }


    if (
        options.body &&
        !(options.body instanceof FormData)
    ) {

        headers.set(
            "Content-Type",
            "application/json"
        );

    }


    const response = await fetch(
        path,
        {
            ...options,
            headers
        }
    );


    const text =
        await response.text();


    let data;


    try {

        data = JSON.parse(text);

    } catch {

        data = {
            raw: text
        };

    }


    if (!response.ok) {

        throw new Error(
            data.detail ||
            data.message ||
            `HTTP ${response.status}`
        );

    }


    return data;
}


// ============================================================
// LOGIN
// ============================================================

loginForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        loginMessage.textContent =
            "Signing in...";


        const body =
            new URLSearchParams();


        body.set(
            "username",
            document.getElementById(
                "username"
            ).value
        );


        body.set(
            "password",
            document.getElementById(
                "password"
            ).value
        );


        body.set(
            "grant_type",
            "password"
        );


        try {

            const response =
                await fetch(
                    "/auth/login",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/x-www-form-urlencoded"
                        },

                        body
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Login failed"
                );

            }


            setToken(
                data.access_token
            );


            loginMessage.textContent = "";


            await loadDashboard();


        } catch (error) {

            loginMessage.textContent =
                error.message;

        }

    }
);


// ============================================================
// LOGOUT
// ============================================================

document
    .getElementById("logoutBtn")
    .addEventListener(
        "click",
        () => {

            clearToken();

            dashboardView
                .classList
                .add("hidden");

            loginView
                .classList
                .remove("hidden");

            loginForm.reset();

        }
    );


// ============================================================
// LOAD DASHBOARD
// ============================================================

async function loadDashboard() {

    try {

        const profile =
            await api(
                "/auth/me"
            );


        loginView
            .classList
            .add("hidden");


        dashboardView
            .classList
            .remove("hidden");


        welcome.textContent =
            `Logged in as ${
                profile.username || "user"
            }`;


        profileBox.textContent =
            JSON.stringify(
                profile,
                null,
                2
            );


        renderActions(
            profile.roles || []
        );


    } catch (error) {

        clearToken();


        loginView
            .classList
            .remove("hidden");


        dashboardView
            .classList
            .add("hidden");


        loginMessage.textContent =
            error.message;

    }
}


// ============================================================
// ACTION BUTTON
// ============================================================

function addAction(
    label,
    path
) {

    const button =
        document.createElement(
            "button"
        );


    button.textContent =
        label;


    button.onclick =
        async () => {

            resultBox.textContent =
                "Loading...";


            try {

                const data =
                    await api(path);


                resultBox.textContent =
                    JSON.stringify(
                        data,
                        null,
                        2
                    );


            } catch (error) {

                resultBox.textContent =
                    error.message;

            }

        };


    actions.appendChild(
        button
    );
}


// ============================================================
// ROLE BASED BUTTONS
// ============================================================

function renderActions(
    roles
) {

    actions.innerHTML = "";


    // Common

    addAction(
        "Check Permission",
        "/permissions/check"
    );


    // ADMIN

    if (
        roles.includes("admin")
    ) {

        addAction(
            "Admin Dashboard",
            "/admin/dashboard"
        );

        addAction(
            "Admin Profile",
            "/admin/profile"
        );

        addAction(
            "Users",
            "/users/"
        );

        addAction(
            "Admin Permission",
            "/permissions/admin"
        );

    }


    // HR

    if (
        roles.includes("hr")
    ) {

        addAction(
            "HR Dashboard",
            "/hr/dashboard"
        );

        addAction(
            "Employees",
            "/hr/employees"
        );

        addAction(
            "HR Permission",
            "/permissions/hr"
        );

    }


    // MANAGER

    if (
        roles.includes("manager")
    ) {

        addAction(
            "Manager Dashboard",
            "/manager/dashboard"
        );

        addAction(
            "Team",
            "/manager/team"
        );

        addAction(
            "Manager Permission",
            "/permissions/manager"
        );

    }


    // EMPLOYEE

    if (
        roles.includes("employee")
    ) {

        addAction(
            "Employee Dashboard",
            "/employee/dashboard"
        );

        addAction(
            "Employee Profile",
            "/employee/profile"
        );

        addAction(
            "Employee Permission",
            "/permissions/employee"
        );

    }
}


// ============================================================
// AUTO LOGIN
// ============================================================

if (getToken()) {

    loadDashboard();

}