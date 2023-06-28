import {
  Form,
  useSearchParams,
  useNavigation,
  useActionData,
  useNavigate,
} from "react-router-dom";
import { json } from "react-router-dom";

import classes from "./AuthForm.module.css";
import { useAuth } from "../hooks/Auth";

const AuthForm = () => {
  const data = useActionData();
  const navigation = useNavigation();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const isLogin = searchParams.get("mode") === "login";
  const isSubmitting = navigation.state === "submitting";
  const { setAuth } = useAuth();

  const login = async (e) => {
    e.preventDefault();
    const url = e.target.action;
    const searchParams = new URL(url).searchParams;
    const mode = searchParams.get("mode") || "login";

    if (mode !== "login" && mode !== "register") {
      throw json({ message: "Unsupported mode." }, { status: 422 });
    }

    const data = new FormData(e.target);
    const authData = {
      email: data.get("email"),
      password: data.get("password"),
    };
    const headers = {
      "Content-Type": "application/json",
    };

    try {
      const response = await fetch("http://localhost:5000/auth/" + mode, {
        method: "POST",
        headers: headers,
        body: JSON.stringify(authData),
      });
      if (response.status === 422 || response.status === 401) {
        return response;
      }

      const resData = await response.json();

      if (resData.status === "fail") {
        alert(resData.message);
        return;
      }

      setAuth(true);

      localStorage.setItem("token", resData.auth_token);
      const expiration = new Date();
      expiration.setHours(expiration.getHours() + 1);
      localStorage.setItem("expiration", expiration.toISOString());
      return navigate("/");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      <Form method="post" onSubmit={login} className={classes.form}>
        <h1>{isLogin ? "Log in" : "Sign up"}</h1>
        {data && data.errors && (
          <ul>
            {Object.values(data.errors).map((err) => (
              <li key={err}>{err}</li>
            ))}
          </ul>
        )}
        {data && data.message && <p>{data.message}</p>}
        <p>
          <label htmlFor="email">Email</label>
          <input id="email" type="email" name="email" required />
        </p>
        <p>
          <label htmlFor="image">Password</label>
          <input id="password" type="password" name="password" required />
        </p>
        <div className="float-end">
          <button disabled={isSubmitting}>
            {isSubmitting ? "Submitting..." : "Submit"}
          </button>
        </div>
      </Form>
    </>
  );
};

export default AuthForm;
