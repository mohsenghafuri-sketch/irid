import { FormEvent, useEffect, useState } from "react";
import { AuthState, getMe, login, logout } from "./api/auth";

type RequestStatus = "idle" | "loading" | "success" | "error";

const initialAuthState: AuthState = {
  authenticated: false,
  user: null,
};

export default function App() {
  const [auth, setAuth] = useState<AuthState>(initialAuthState);
  const [email, setEmail] = useState("testuser1@iridco.ir");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<RequestStatus>("loading");
  const [message, setMessage] = useState("در حال بررسی نشست کاربر...");

  useEffect(() => {
    void refreshAuth();
  }, []);

  async function refreshAuth() {
    setStatus("loading");

    try {
      const nextAuth = await getMe();
      setAuth(nextAuth);
      setStatus("success");
      setMessage(nextAuth.authenticated ? "نشست فعال است." : "کاربر وارد نشده است.");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "خطا در دریافت وضعیت کاربر.");
    }
  }

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setStatus("loading");
    setMessage("در حال ورود...");

    try {
      const nextAuth = await login(email, password);
      setAuth(nextAuth);
      setStatus("success");
      setMessage("ورود موفق بود.");
      setPassword("");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "ورود ناموفق بود.");
    }
  }

  async function handleLogout() {
    setStatus("loading");
    setMessage("در حال خروج...");

    try {
      const nextAuth = await logout();
      setAuth(nextAuth);
      setStatus("success");
      setMessage("خروج موفق بود.");
    } catch (error) {
      setStatus("error");
      setMessage(error instanceof Error ? error.message : "خروج ناموفق بود.");
    }
  }

  return (
    <main className="app-shell">
      <section className="auth-panel">
        <div className="panel-header">
          <div>
            <p className="eyebrow">IRID Automation</p>
            <h1>ورود به سامانه</h1>
          </div>
          <button className="ghost-button" type="button" onClick={refreshAuth}>
            بررسی نشست
          </button>
        </div>

        <div className={`status-strip ${status}`}>
          <span>{message}</span>
        </div>

        {auth.authenticated && auth.user ? (
          <div className="dashboard">
            <div>
              <p className="label">کاربر فعال</p>
              <h2>{auth.user.email}</h2>
            </div>

            <dl className="user-grid">
              <div>
                <dt>شناسه</dt>
                <dd>{auth.user.id}</dd>
              </div>
              <div>
                <dt>نام کامل</dt>
                <dd>{auth.user.full_name || "ثبت نشده"}</dd>
              </div>
              <div>
                <dt>Staff</dt>
                <dd>{auth.user.is_staff ? "بله" : "خیر"}</dd>
              </div>
              <div>
                <dt>Superuser</dt>
                <dd>{auth.user.is_superuser ? "بله" : "خیر"}</dd>
              </div>
            </dl>

            <button className="danger-button" type="button" onClick={handleLogout}>
              خروج
            </button>
          </div>
        ) : (
          <form className="login-form" onSubmit={handleLogin}>
            <label>
              ایمیل
              <input
                autoComplete="username"
                dir="ltr"
                type="email"
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                required
              />
            </label>

            <label>
              رمز عبور
              <input
                autoComplete="current-password"
                dir="ltr"
                type="password"
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                required
              />
            </label>

            <button className="primary-button" type="submit" disabled={status === "loading"}>
              ورود
            </button>
          </form>
        )}
      </section>
    </main>
  );
}
