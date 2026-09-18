import { useState } from "react";
import "./AdminLogin.css";

function AdminLogin({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (event) => {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const formData = new URLSearchParams();

      formData.append("username", username);
      formData.append("password", password);

      const response = await fetch(
        "http://127.0.0.1:8000/admin/login",
        {
          method: "POST",
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Login failed."
        );
      }

      localStorage.setItem(
        "admin_access_token",
        data.access_token
      );

      onLogin(data.access_token);
    } catch (error) {
      setError(
        error.message ||
          "Unable to login. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="admin-login-page">

      <div className="admin-login-card">

        <div className="admin-login-icon">
          🔐
        </div>

        <div className="admin-login-header">
          <div className="admin-login-badge">
            ADMIN PANEL
          </div>

          <h1>Welcome Back</h1>

          <p>
            Sign in to access your Resume Analyzer
            analytics dashboard.
          </p>
        </div>

        <form
          className="admin-login-form"
          onSubmit={handleLogin}
        >

          <div className="admin-login-field">
            <label htmlFor="admin-username">
              Username
            </label>

            <input
              id="admin-username"
              type="text"
              value={username}
              onChange={(event) =>
                setUsername(event.target.value)
              }
              placeholder="Enter admin username"
              autoComplete="username"
              required
            />
          </div>

          <div className="admin-login-field">
            <label htmlFor="admin-password">
              Password
            </label>

            <input
              id="admin-password"
              type="password"
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter admin password"
              autoComplete="current-password"
              required
            />
          </div>

          {error && (
            <div className="admin-login-error">
              {error}
            </div>
          )}

          <button
            type="submit"
            className="admin-login-button"
            disabled={loading}
          >
            {loading
              ? "Signing in..."
              : "Sign In to Dashboard"}
          </button>

        </form>

        <div className="admin-login-footer">
          <span>🔒</span>
          Secure administrator access
        </div>

      </div>

    </div>
  );
}

export default AdminLogin;