import { NavLink } from "react-router-dom";

const MoviesNavigation = () => {
  return (
    <ul className="nav nav-pills justify-content-center">
      <li className="nav-item">
        <NavLink
          to="/nowshowing"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
          end
        >
          Now Showing
        </NavLink>
      </li>
      <li className="nav-item">
        <NavLink
          to="/comingsoon"
          className={({ isActive }) =>
            isActive ? "nav-link active" : "nav-link"
          }
          end
        >
          Coming Soon
        </NavLink>
      </li>
    </ul>
  );
};

export default MoviesNavigation;
