import { NavLink, Form, useNavigate, useSubmit, Link } from "react-router-dom";

import { tokenLoader } from "../utils/auth";
import { useAuth } from "../hooks/Auth";
import "../css/Navbar.css";
import apiUrl from "../config";

const AuthNavbar = () => {
  const { setAuth, user, setUser } = useAuth();
  const navigate = useNavigate();
  const submit = useSubmit();

  const logout = async (e) => {
    e.preventDefault();
    const token = tokenLoader();
    if (!token || token === "EXPIRED") {
      submit(null, { action: "/logout", method: "post" });
      setAuth(false);
      setUser(null);
      localStorage.removeItem("token");
      localStorage.removeItem("expiration");
      return navigate("/");
    }
    const headers = {
      Authorization: `Basic ${token}`,
      withCredentials: true,
    };
    try {
      const response = await fetch(`${apiUrl}/auth/logout`, {
        method: "POST",
        headers: headers,
      });

      if (response.status === 422 || response.status === 401) {
        setAuth(false);
        setUser(null);
        localStorage.removeItem("token");
        localStorage.removeItem("expiration");
        return navigate("/");
      }

      const resData = await response.json();

      if (resData.status === "fail") {
        console.error(resData.message);
        setAuth(false);
        setUser(null);
        localStorage.removeItem("token");
        localStorage.removeItem("expiration");
        return navigate("/");
      }
      localStorage.removeItem("token");
      localStorage.removeItem("expiration");
      setAuth(false);
      return navigate("/");
    } catch (error) {
      console.error(error);
      setAuth(false);
      setUser(null);
      localStorage.removeItem("token");
      localStorage.removeItem("expiration");
      return navigate("/");
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light custom-navbar">
      <NavLink to="/" className="navbar-brand">
        What Movie?
      </NavLink>
      <ul className="navbar-nav ms-auto">
        <li className="nav-item dropdown">
          <a
            className="nav-link dropdown-toggle"
            href="/#"
            id="navbarDropdown"
            role="button"
            data-bs-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            Welcome {user && user.email && user.email.split("@")[0]}
          </a>
          <div
            className="dropdown-menu dropdown-menu-end"
            aria-labelledby="navbarDropdown"
          >
            <Link className="dropdown-item" to="favourites">
              View favourites
            </Link>
            <div className="dropdown-divider"></div>
            <Form onSubmit={logout} method="post">
              <button className="dropdown-item">Log out</button>
            </Form>
          </div>
        </li>
      </ul>
    </nav>
  );
};

export default AuthNavbar;
