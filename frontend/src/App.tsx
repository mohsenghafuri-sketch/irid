import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { getMe, logout } from './api/auth';
import InboxPage from './pages/InboxPage';
import LoginPage from './pages/LoginPage';

const App: React.FC = () => {
  const [auth, setAuth] = useState({ authenticated: false, user: null as any });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMe().then(data => setAuth({ authenticated: true, user: data })).catch(() => setAuth({ authenticated: false, user: null })).finally(() => setLoading(false));
  }, []);

  const handleLogout = async () => {
    await logout();
    window.location.href = '/';
  };

  if (loading) return <div style={{ padding: '50px', textAlign: 'center' }}>در حال بارگذاری...</div>;

  return (
    <Router>
      <div style={{ minHeight: '100vh', backgroundColor: '#f4f7f6', direction: 'rtl', fontFamily: 'Tahoma' }}>
        <nav style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 30px', backgroundColor: '#2c3e50', color: 'white', alignItems: 'center' }}>
          <div><strong>اتوماسیون IRID</strong> | <Link to="/" style={{ color: 'white' }}>داشبورد</Link></div>
          {auth.authenticated ? <button onClick={handleLogout}>خروج</button> : <Link to="/login" style={{ color: 'white' }}>ورود</Link>}
        </nav>
        <div style={{ padding: '30px' }}>
          <Routes>
            <Route path="/" element={
              <div style={{ background: 'white', padding: '25px' }}>
                <h2>داشبورد</h2>
                {auth.authenticated ? <p>سلام {auth.user?.email}</p> : <p>لطفاً <Link to="/login">وارد شوید</Link></p>}
              </div>
            } />
            <Route path="/inbox" element={<InboxPage />} />
            <Route path="/login" element={<LoginPage />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
