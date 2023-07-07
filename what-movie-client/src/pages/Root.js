import { useEffect } from "react";
import { Outlet, useLoaderData, useSubmit } from "react-router-dom";

import AuthNavbar from "../components/AuthNavbar";
import NotAuthNavbar from "../components/NotAuthNavbar";
import { getTokenDuration } from "../utils/auth";
import { useAuth } from "../hooks/Auth";

const RootLayout = () => {
  const token = useLoaderData();
  const submit = useSubmit();
  const { auth, setAuth, setUser } = useAuth();

  useEffect(() => {
    if (!token) {
      setAuth(false);
      setUser(null);
      return;
    }

    if (token === "EXPIRED") {
      console.log("HERE");
      submit(null, { action: "/logout", method: "post" });
      alert("Token expired, please sign in again");
      setAuth(false);
      setUser(null);
      return;
    }

    const tokenDuration = getTokenDuration();
    console.log(tokenDuration);
  }, [setAuth, setUser]);

  return (
    <>
      {auth ? <AuthNavbar /> : <NotAuthNavbar />}
      <main>
        <Outlet />
      </main>
    </>
  );
};

export default RootLayout;
