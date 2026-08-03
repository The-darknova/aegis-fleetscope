import React from 'react';
import './Pages.css';

const PolicyManagement: React.FC = () => {
  return (
    <div className="page-wrapper">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1>Policy Management</h1>
          <p className="text-muted">Configure and distribute SCAP content across the fleet</p>
        </div>
        <button className="btn btn-primary">Upload SCAP Content</button>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Policy Name</th>
              <th>Profile ID</th>
              <th>Target OS</th>
              <th>Assigned Hosts</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{fontWeight: 500}}>Ubuntu 24.04 Baseline</td>
              <td>xccdf_org.ssgproject.content_profile_cis_level1_server</td>
              <td>Ubuntu 24.04</td>
              <td>12</td>
              <td><span className="badge badge-success">Active</span></td>
            </tr>
            <tr>
              <td style={{fontWeight: 500}}>RHEL 9 STIG</td>
              <td>xccdf_org.ssgproject.content_profile_stig</td>
              <td>RHEL 9</td>
              <td>8</td>
              <td><span className="badge badge-warning">Draft</span></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default PolicyManagement;
