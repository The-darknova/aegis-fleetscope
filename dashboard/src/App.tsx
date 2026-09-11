import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import FleetOverview from './pages/FleetOverview';
import HostInventory from './pages/HostInventory';
import HistoricalReports from './pages/HistoricalReports';
import PolicyManagement from './pages/PolicyManagement';
import { client } from './api/client.gen';
import { login } from './api/sdk.gen';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    client.setConfig({ baseUrl: API_BASE_URL });
    
    if (token) {
      client.setConfig({
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
    }

    // Set up interceptor for 401 errors
    const interceptor = client.interceptors.response.use(
      async (response, request, options) => {
        if (response.status === 401) {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken) {
            try {
              const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh_token: refreshToken })
              });
              if (res.ok) {
                const data = await res.json();
                setToken(data.access_token);
                localStorage.setItem('token', data.access_token);
                
                // Retry the original request
                const headers = new Headers(request.headers);
                headers.set('Authorization', `Bearer ${data.access_token}`);
                
                const requestInit: RequestInit = {
                  method: request.method,
                  headers: headers,
                };
                
                if (request.method !== 'GET' && request.method !== 'HEAD') {
                  const opts = options as any;
                  requestInit.body = opts.serializedBody !== undefined ? opts.serializedBody : opts.body;
                }
                
                return fetch(new Request(request.url, requestInit));
              }
            } catch (e) {
              console.error("Refresh token failed", e);
            }
          }
          // If refresh fails or no refresh token, logout
          setToken(null);
          localStorage.removeItem('token');
          localStorage.removeItem('refresh_token');
        }
        return response;
      }
    );

    return () => {
      client.interceptors.response.eject(interceptor);
    };
  }, [token]);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await login({ body: { username, password } });
      if (res.data) {
        const data = res.data as any; // Bypass TS checking for new fields
        setToken(data.access_token);
        localStorage.setItem('token', data.access_token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
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
