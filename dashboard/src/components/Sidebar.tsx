import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Server, History, ShieldAlert } from 'lucide-react';
import './Sidebar.css';

const Sidebar: React.FC = () => {
  return (
    <aside className="sidebar glass-panel">
      <div className="sidebar-header">
        <ShieldAlert className="logo-icon" size={28} />
        <h2 className="logo-text">Aegis FleetScope</h2>
      </div>
      
      <nav className="sidebar-nav">
        <NavLink 
          to="/" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <LayoutDashboard size={20} />
          <span>Fleet Overview</span>
        </NavLink>
        
        <NavLink 
          to="/inventory" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <Server size={20} />
          <span>Host Inventory</span>
        </NavLink>
        
        <NavLink 
          to="/reports" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <History size={20} />
          <span>Historical Reports</span>
        </NavLink>
        
        <NavLink 
          to="/policies" 
          className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
        >
          <ShieldAlert size={20} />
          <span>Policy Management</span>
        </NavLink>
      </nav>
      
      <div className="sidebar-footer">
        <div className="status-indicator online"></div>
        <span className="text-muted" style={{fontSize: '0.875rem'}}>Agent Gateway Online</span>
      </div>
    </aside>
  );
};

export default Sidebar;
