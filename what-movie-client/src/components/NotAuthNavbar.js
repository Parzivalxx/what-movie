import { NavLink } from "react-router-dom";

import "../css/Navbar.css";

const NotAuthNavbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
      <NavLink to="/" className="navbar-brand">
        What Movie?
      </NavLink>
      <button
        className="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span className="navbar-toggler-icon"></span>
      </button>
      <div
        className="collapse navbar-collapse justify-content-end"
        id="navbarSupportedContent"
      >
        <ul className="navbar-nav">
          <li className="nav-item">
            <NavLink to="/auth?mode=login" className="nav-link">
              Login
            </NavLink>
          </li>
          <li className="nav-item">
            <NavLink to="/auth?mode=register" className="nav-link">
              Sign up
            </NavLink>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default NotAuthNavbar;
