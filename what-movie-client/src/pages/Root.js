import { useEffect } from "react";
import { Outlet, useLoaderData, useSubmit } from "react-router-dom";

import AuthNavbar from "../components/AuthNavbar";
import NotAuthNavbar from "../components/NotAuthNavbar";
import { getTokenDuration } from "../utils/auth";
import { useAuth } from "../hooks/Auth";

const RootLayout = () => {
  const token = useLoaderData();
  const submit = useSubmit();
  const { auth } = useAuth();

  useEffect(() => {
    if (!token) {
      return;
    }

    if (token === "EXPIRED") {
      submit(null, { action: "/logout", method: "post" });
      return;
    }

    const tokenDuration = getTokenDuration();
    console.log(tokenDuration);

    setTimeout(() => {
      submit(null, { action: "/logout", method: "post" });
    }, tokenDuration);
  }, [token, submit]);

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
