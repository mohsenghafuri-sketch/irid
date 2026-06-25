import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api/auth';

const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login({ email, password });
      window.location.href = '/'; // رفرش کامل برای ست شدن وضعیت احراز هویت
    } catch (err) {
      setError('خطا در ورود: ایمیل یا رمز عبور اشتباه است.');
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: '50px auto', padding: '30px', background: 'white', borderRadius: '8px', boxShadow: '0 2px 10px rgba(0,0,0,0.1)' }}>
      <h2 style={{ textAlign: 'center' }}>ورود به اتوماسیون IRID</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input type="email" placeholder="ایمیل" value={email} onChange={(e) => setEmail(e.target.value)} style={{ padding: '10px' }} required />
        <input type="password" placeholder="رمز عبور" value={password} onChange={(e) => setPassword(e.target.value)} style={{ padding: '10px' }} required />
        {error && <p style={{ color: 'red', fontSize: '0.9rem' }}>{error}</p>}
        <button type="submit" style={{ padding: '10px', background: '#2c3e50', color: 'white', border: 'none', cursor: 'pointer' }}>ورود</button>
      </form>
    </div>
  );
};

export default LoginPage;
