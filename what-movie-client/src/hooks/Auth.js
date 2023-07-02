import { createContext, useContext, useEffect, useState } from "react";
import { tokenLoader } from "../utils/auth";

const AuthContext = createContext({
  auth: null,
  setAuth: () => {},
  user: null,
});

export const useAuth = () => useContext(AuthContext);

const AuthProvider = ({ children }) => {
  const [auth, setAuth] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = tokenLoader();
    console.log("TOKEN: " + token);
    if (!token || token === "EXPIRED") {
      setAuth(false);
      setUser(null);
      return;
    }
    const headers = {
      "Content-Type": "application/json",
      Authorization: `Basic ${token}`,
    };
    const isAuth = async () => {
      try {
        const res = await fetch("http://localhost:5000/auth/status", {
          method: "GET",
          headers: headers,
        });
        if (!res.ok) {
          setAuth(false);
          setUser(null);
          return;
        }
        const resData = await res.json();
        setAuth(true);
        setUser(resData.data);
      } catch (error) {
        console.error(error);
        setAuth(false);
        setUser(null);
      }
    };
    isAuth();
  }, [auth]);

  return (
    <AuthContext.Provider value={{ auth, setAuth, user, setUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
