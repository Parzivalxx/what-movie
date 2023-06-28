import { RouterProvider, createBrowserRouter } from "react-router-dom";

import ErrorPage from "./pages/Error";
import RootLayout from "./pages/Root";
import AuthenticationPage from "./pages/Authentication";
import { tokenLoader } from "./utils/auth";
import MoviesRootLayout from "./pages/MoviesRoot";
import NowShowingMoviesPage, {
  loader as nowShowingMoviesLoader,
} from "./pages/Movies";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    loader: tokenLoader,
    children: [
      {
        path: "",
        element: <MoviesRootLayout />,
        children: [
          {
            path: "",
            element: <NowShowingMoviesPage />,
            loader: nowShowingMoviesLoader,
          },
        ],
      },
      {
        path: "auth",
        element: <AuthenticationPage />,
      },
    ],
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
