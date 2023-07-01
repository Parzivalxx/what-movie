import { RouterProvider, createBrowserRouter } from "react-router-dom";

import ErrorPage from "./pages/Error";
import RootLayout from "./pages/Root";
import AuthenticationPage from "./pages/Authentication";
import { tokenLoader } from "./utils/auth";
import MoviesRootLayout from "./pages/MoviesRoot";
import { action as logoutAction } from "./pages/Logout";
import MovieDetailPage, {
  loader as movieDetailsLoader,
} from "./pages/MovieDetail";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    loader: tokenLoader,
    children: [
      {
        index: true,
        element: <MoviesRootLayout />,
      },
      {
        path: "auth",
        element: <AuthenticationPage />,
      },
      {
        path: "logout",
        action: logoutAction,
      },
      {
        path: "movies",
        children: [
          {
            path: ":movieId",
            id: "movie-showtimes",
            element: <MovieDetailPage />,
            loader: movieDetailsLoader,
          },
        ],
      },
    ],
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
