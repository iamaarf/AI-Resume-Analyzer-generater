function AdminLogout() {
  const handleLogout = () => {
    localStorage.removeItem(
      "admin_access_token"
    );

    window.location.href = "/admin";
  };

  return (
    <button
      type="button"
      className="admin-logout-button"
      onClick={handleLogout}
    >
      Logout
    </button>
  );
}

export default AdminLogout;