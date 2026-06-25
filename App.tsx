import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";

const pageStyle: React.CSSProperties = {
  padding: "24px",
  direction: "rtl",
  fontFamily: "Tahoma, Arial, sans-serif",
};

const cardStyle: React.CSSProperties = {
  background: "#ffffff",
  padding: "24px",
  borderRadius: "8px",
  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
};

const Dashboard: React.FC = () => {
  return (
    <div style={pageStyle}>
      <div style={cardStyle}>
        <h1>داشبورد</h1>
        <p>اگر این صفحه را می‌بینید، یعنی React و Vite دوباره سالم بالا آمده‌اند.</p>

        <Link to="/inbox">
          <button
            style={{
              backgroundColor: "#3498db",
              color: "#fff",
              border: "none",
              padding: "10px 16px",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            برو به کارتابل
          </button>
        </Link>
      </div>
    </div>
  );
};

const Inbox: React.FC = () => {
  return (
    <div style={pageStyle}>
      <div style={cardStyle}>
        <h1>کارتابل ورودی</h1>
        <p>اگر این صفحه را می‌بینید، یعنی Router درست کار می‌کند.</p>

        <Link to="/">
          <button
            style={{
              backgroundColor: "#2c3e50",
              color: "#fff",
              border: "none",
              padding: "10px 16px",
              borderRadius: "4px",
              cursor: "pointer",
            }}
          >
            برگشت به داشبورد
          </button>
        </Link>
      </div>
    </div>
  );
};

const App: React.FC = () => {
  return (
    <Router>
      <div
        style={{
          minHeight: "100vh",
          backgroundColor: "#f4f7f6",
          direction: "rtl",
          fontFamily: "Tahoma, Arial, sans-serif",
        }}
      >
        <nav
          style={{
            padding: "12px 24px",
            backgroundColor: "#2c3e50",
            color: "#ffffff",
            display: "flex",
            gap: "16px",
            alignItems: "center",
          }}
        >
          <strong>سامانه IRID</strong>

          <Link to="/" style={{ color: "#ffffff", textDecoration: "none" }}>
            داشبورد
          </Link>

          <Link to="/inbox" style={{ color: "#ffffff", textDecoration: "none" }}>
            کارتابل
          </Link>
        </nav>

        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/inbox" element={<Inbox />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
EOF
