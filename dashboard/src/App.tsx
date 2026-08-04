import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import FleetOverview from './pages/FleetOverview';
import HostInventory from './pages/HostInventory';
import HistoricalReports from './pages/HistoricalReports';
import PolicyManagement from './pages/PolicyManagement';
import { client } from './api/client.gen';
import { login } from './api/sdk.gen';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      client.setConfig({
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      // Set baseUrl just in case
      client.setConfig({ baseUrl: 'http://localhost:8000/api/v1' });
    }
  }, [token]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      client.setConfig({ baseUrl: 'http://localhost:8000/api/v1' });
      const res = await login({ body: { username, password } });
      if (res.data) {
        setToken(res.data.access_token);
        localStorage.setItem('token', res.data.access_token);
        setError('');
      }
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  if (!token) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', background: '#0a0a0a', color: 'white' }}>
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem', background: '#1a1a1a', padding: '2rem', borderRadius: '8px' }}>
          <h2>Aegis Login</h2>
          {error && <div style={{ color: 'red' }}>{error}</div>}
          <input 
            type="text" 
            placeholder="Username" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            style={{ padding: '0.5rem' }}
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            style={{ padding: '0.5rem' }}
          />
          <button type="submit" style={{ padding: '0.5rem', background: '#3b82f6', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>Login</button>
        </form>
      </div>
    );
  }

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<FleetOverview />} />
          <Route path="inventory" element={<HostInventory />} />
          <Route path="reports" element={<HistoricalReports />} />
          <Route path="policies" element={<PolicyManagement />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
