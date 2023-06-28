import { RouterProvider, createBrowserRouter } from "react-router-dom";

import ErrorPage from "./pages/Error";
import HomePage from "./pages/Home";
import RootLayout from "./pages/Root";
import AuthenticationPage from "./pages/Authentication";
import MoviesPage from "./pages/Movies";
import { tokenLoader } from "./utils/auth";

const router = createBrowserRouter([
  {
    path: "/",
    element: <RootLayout />,
    errorElement: <ErrorPage />,
    id: "root",
    loader: tokenLoader,
    children: [
      { index: true, element: <HomePage /> },
      {
        path: "auth",
        element: <AuthenticationPage />,
      },
      {
        path: "movies",
        element: <MoviesPage />,
      },
    ],
  },
]);

const App = () => {
  return <RouterProvider router={router} />;
};

export default App;
