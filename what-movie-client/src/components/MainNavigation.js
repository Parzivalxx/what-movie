import { Form, NavLink, useRouteLoaderData } from "react-router-dom";

const MainNavigation = () => {
  const token = useRouteLoaderData("root");

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
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
        <span class="navbar-toggler-icon"></span>
      </button>
      <div
        className="collapse navbar-collapse justify-content-end"
        id="navbarSupportedContent"
      >
        <ul class="navbar-nav">
          {!token && (
            <>
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
            </>
          )}
          {token && (
            <li className="nav-item dropdown">
              <a
                className="nav-link dropdown-toggle"
                href="#"
                id="navbarDropdown"
                role="button"
                data-bs-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false"
              >
                Dropdown
              </a>
              <div className="dropdown-menu" aria-labelledby="navbarDropdown">
                <a className="dropdown-item" href="#">
                  View favourites
                </a>
                <div className="dropdown-divider"></div>
                <Form action="/logout" method="post">
                  <button>Log out</button>
                </Form>
              </div>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default MainNavigation;
