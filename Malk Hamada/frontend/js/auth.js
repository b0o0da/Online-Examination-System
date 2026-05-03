const registerForm = document.getElementById("registerForm");
const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");

if (registerForm) {
  registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const userData = {
      username: document.getElementById("username").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value,
      role: document.getElementById("role").value
    };

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(userData)
      });

      const data = await response.json();

      if (!response.ok) {
        message.textContent = data.detail || "Registration failed";
        return;
      }

      message.style.color = "green";
      message.textContent = "Registration successful. Please login.";

      setTimeout(() => {
        window.location.href = "login.html";
      }, 1000);

    } catch (error) {
      message.textContent = "Server error. Please try again.";
    }
  });
}

if (loginForm) {
  loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const loginData = {
      email: document.getElementById("loginEmail").value,
      password: document.getElementById("loginPassword").value
    };

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(loginData)
      });

      const data = await response.json();

      if (!response.ok) {
        message.textContent = data.detail || "Login failed";
        return;
      }

      localStorage.setItem("token", data.access_token);
      window.location.href = "exams.html";

    } catch (error) {
      message.textContent = "Server error. Please try again.";
    }
  });
}