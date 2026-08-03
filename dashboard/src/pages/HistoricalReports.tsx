import React from 'react';
import './Pages.css';

const HistoricalReports: React.FC = () => {
  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Historical Reports</h1>
        <p className="text-muted">Review past OpenSCAP assessment results</p>
      </div>

      <div className="glass-panel" style={{ padding: '24px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Scan ID</th>
              <th>Target Host</th>
              <th>Policy Profile</th>
              <th>Date</th>
              <th>Compliance Score</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>SCAN-8392A</td>
              <td>web-server-prod-01</td>
              <td>CIS Ubuntu 24.04 L1</td>
              <td>Aug 03, 2026</td>
              <td><span className="text-success" style={{fontWeight: 'bold'}}>98%</span></td>
              <td><button className="btn btn-secondary">View Report</button></td>
            </tr>
            <tr>
              <td>SCAN-8391B</td>
              <td>db-primary-eu</td>
              <td>STIG RHEL 9</td>
              <td>Aug 02, 2026</td>
              <td><span className="text-warning" style={{fontWeight: 'bold'}}>74%</span></td>
              <td><button className="btn btn-secondary">View Report</button></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoricalReports;
