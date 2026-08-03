import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import './Layout.css';

const Layout: React.FC = () => {
  return (
    <div className="layout-container">
      <Sidebar />
      <main className="main-content">
        <header className="top-header glass-panel">
          <div className="header-breadcrumbs">
            <span className="text-muted">Aegis</span>
            <span className="text-muted mx-2">/</span>
            <span style={{fontWeight: 500}}>Dashboard</span>
          </div>
          <div className="header-actions">
            <button className="btn btn-secondary">Settings</button>
            <div className="avatar">Admin</div>
          </div>
        </header>
        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default Layout;
