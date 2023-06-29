import MoviesPage from "./Movies";
import PageContent from "../components/PageContent";

const MoviesRootLayout = () => {
  return (
    <>
      <PageContent title="Welcome to What Movie!">
        <p>
          Browse the latest movies available now or coming soon to cinemas near
          you!
        </p>
        <MoviesPage />
      </PageContent>
    </>
  );
};

export default MoviesRootLayout;
