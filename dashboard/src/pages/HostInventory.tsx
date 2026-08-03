import React from 'react';
import './Pages.css';

const HostInventory: React.FC = () => {
  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Host Inventory</h1>
        <p className="text-muted">Manage and monitor connected agents</p>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Hostname</th>
              <th>OS / Version</th>
              <th>Architecture</th>
              <th>Status</th>
              <th>Last Seen</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{fontWeight: 500}}>web-server-prod-01</td>
              <td>Ubuntu 24.04</td>
              <td>x86_64</td>
              <td><span className="badge badge-success">Online</span></td>
              <td>2 mins ago</td>
              <td><button className="btn btn-secondary">Details</button></td>
            </tr>
            <tr>
              <td style={{fontWeight: 500}}>db-primary-eu</td>
              <td>RHEL 9.2</td>
              <td>aarch64</td>
              <td><span className="badge badge-warning">Syncing</span></td>
              <td>10 mins ago</td>
              <td><button className="btn btn-secondary">Details</button></td>
            </tr>
            <tr>
              <td style={{fontWeight: 500}}>cache-node-04</td>
              <td>Debian 12</td>
              <td>x86_64</td>
              <td><span className="badge badge-danger">Offline</span></td>
              <td>2 days ago</td>
              <td><button className="btn btn-secondary">Details</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HostInventory;
