import { createContext, useContext, useEffect, useState } from "react";

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
    const token = localStorage.getItem("token");
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
        const resData = await res.json();
        setUser(resData.data);
      } catch (error) {
        console.error(error);
        setUser(null);
      }
    };
    isAuth();
  }, [auth]);

  return (
    <AuthContext.Provider value={{ auth, setAuth, user }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthProvider;
