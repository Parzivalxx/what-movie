import { Outlet } from "react-router-dom";

import MoviesNavigation from "../components/MoviesNavigation";
import PageContent from "../components/PageContent";

const MoviesRootLayout = () => {
  return (
    <>
      <PageContent title="Welcome to What Movie!">
        <p>
          Browse the latest movies available now or coming soon to cinemas near
          you!
        </p>
        <MoviesNavigation />
        <Outlet />
      </PageContent>
    </>
  );
};

export default MoviesRootLayout;
