import React, { useEffect, useState } from 'react';
import './Pages.css';
import { listReports } from '../api/sdk.gen';

const HistoricalReports: React.FC = () => {
  const [reports, setReports] = useState<any[]>([]);

  useEffect(() => {
    async function fetchReports() {
      try {
        const res = await listReports();
        if (res.data) setReports(res.data);
      } catch (err) {
        console.error("Failed to fetch reports", err);
      }
    }
    fetchReports();
  }, []);

  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Compliance Reports</h1>
        <p className="text-muted">History of all OpenSCAP evaluations</p>
      </div>

      <div className="glass-panel table-container">
        <table>
          <thead>
            <tr>
              <th>Report ID</th>
              <th>Agent ID</th>
              <th>Timestamp</th>
              <th>Compliance Score</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {reports.map((report) => (
              <tr key={report.id}>
                <td>{report.id}</td>
                <td>{report.agent_id}</td>
                <td>{report.timestamp ? new Date(report.timestamp).toLocaleString() : 'N/A'}</td>
                <td>
                  <span className={`badge ${report.score >= 90 ? 'badge-success' : 'badge-error'}`}>
                    {report.score.toFixed(1)}%
                  </span>
                </td>
                <td>
                  <button className="text-btn">View HTML</button>
                </td>
              </tr>
            ))}
            {reports.length === 0 && (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center' }}>No reports found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoricalReports;
