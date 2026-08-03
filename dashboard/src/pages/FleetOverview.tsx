import React from 'react';
import './Pages.css';

const FleetOverview: React.FC = () => {
  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Fleet Overview</h1>
        <p className="text-muted">Real-time compliance visibility across your infrastructure</p>
      </div>
      
      <div className="metrics-grid">
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Total Agents</h3>
          <div className="metric-value">24</div>
          <div className="metric-trend text-success">+3 this week</div>
        </div>
        
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Average Compliance</h3>
          <div className="metric-value">92%</div>
          <div className="metric-trend text-warning">-1% this week</div>
        </div>
        
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Failed Rules</h3>
          <div className="metric-value text-danger">15</div>
          <div className="metric-trend text-danger">+2 this week</div>
        </div>
      </div>

      <div className="dashboard-charts glass-panel" style={{ marginTop: '24px', padding: '24px', minHeight: '300px' }}>
        <h3>Compliance Trends</h3>
        <div className="placeholder-chart">
          {/* Chart placeholder */}
          <span className="text-muted">Chart visualization will render here</span>
        </div>
      </div>
    </div>
  );
};

export default FleetOverview;
