import { NavLink, Form, useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/Auth";

const AuthNavbar = () => {
  const { setAuth, user } = useAuth();
  const navigate = useNavigate();

  const logout = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem("token");
    const headers = {
      Authorization: `Basic ${token}`,
      withCredentials: true,
    };
    try {
      const response = await fetch("http://localhost:5000/auth/logout", {
        method: "POST",
        headers: headers,
      });

      if (response.status === 422 || response.status === 401) {
        return response;
      }

      const resData = await response.json();

      if (resData.status === "fail") {
        alert(resData.message);
        return;
      }
      localStorage.removeItem("token");
      localStorage.removeItem("expiration");
      setAuth(false);
      return navigate("/");
    } catch (error) {
      console.error(error);
      return;
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light ps-5 pe-5">
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
            <a className="dropdown-item" href="/#">
              View favourites
            </a>
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
