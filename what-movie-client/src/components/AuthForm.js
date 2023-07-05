import {
  Form,
  useSearchParams,
  useNavigation,
  useActionData,
  useNavigate,
  json,
} from "react-router-dom";
import { useState } from "react";
import { Alert } from "react-bootstrap";

import "../css/AuthForm.css";
import { useAuth } from "../hooks/Auth";

const AuthForm = () => {
  const data = useActionData();
  const navigation = useNavigation();
  const navigate = useNavigate();

  const [searchParams] = useSearchParams();
  const [error, setError] = useState(null);
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
        setError(resData.message);
        return;
      }

      setAuth(true);

      localStorage.setItem("token", resData.auth_token);
      const expiration = new Date();
      expiration.setSeconds(expiration.getSeconds() + 30 * 60 * 60 * 24);
      localStorage.setItem("expiration", expiration.toISOString());
      return navigate("/");
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <>
      {error && (
        <Alert
          className="form"
          key="danger"
          onClose={() => setError(null)}
          dismissible
          variant="danger"
        >
          {error}
        </Alert>
      )}
      <Form method="post" onSubmit={login} className="form">
        <h1>{isLogin ? "Log in" : "Sign up"}</h1>
        {data && data.errors && (
          <ul>
            {Object.values(data.errors).map((err) => (
              <li key={err}>{err}</li>
            ))}
          </ul>
        )}
        {data && data.message && <p>{data.message}</p>}
        <p className="my-4">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" name="email" required />
        </p>
        <p>
          <label htmlFor="image">Password</label>
          <input id="password" type="password" name="password" required />
        </p>
        <div>
          <button
            className="btn btn-primary mt-4 w-100"
            disabled={isSubmitting}
          >
            {isSubmitting ? "Submitting..." : "Submit"}
          </button>
        </div>
      </Form>
    </>
  );
};

export default AuthForm;
