import { StrictMode, useState } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";

import App from "./App.jsx";
import AdminDashboard from "./AdminDashboard.jsx";
import AdminLogin from "./AdminLogin.jsx";
import ResumeBuilder from "./ResumeBuilder.jsx";

function AdminApp() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    Boolean(
      localStorage.getItem("admin_access_token")
    )
  );

  const handleLogin = () => {
    setIsLoggedIn(true);
  };

  if (!isLoggedIn) {
    return (
      <AdminLogin
        onLogin={handleLogin}
      />
    );
  }

  return <AdminDashboard />;
}

const isAdminPage =
  window.location.pathname === "/admin";

const isResumeBuilderPage =
  window.location.pathname === "/resume-builder";

createRoot(
  document.getElementById("root")
).render(
  <StrictMode>
    {isAdminPage ? (
      <AdminApp />
    ) : isResumeBuilderPage ? (
      <ResumeBuilder />
    ) : (
      <App />
    )}
  </StrictMode>
);