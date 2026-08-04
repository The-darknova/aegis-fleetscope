import React, { useEffect, useState } from 'react';
import './Pages.css';
import { listAgents } from '../api/sdk.gen';

const HostInventory: React.FC = () => {
  const [agents, setAgents] = useState<any[]>([]);

  useEffect(() => {
    async function fetchAgents() {
      try {
        const res = await listAgents();
        if (res.data) setAgents(res.data);
      } catch (err) {
        console.error("Failed to fetch agents", err);
      }
    }
    fetchAgents();
  }, []);

  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Host Inventory</h1>
        <button className="primary-btn">Add Host</button>
      </div>

      <div className="glass-panel table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Hostname</th>
              <th>OS / Version</th>
              <th>Architecture</th>
              <th>Last Seen</th>
            </tr>
          </thead>
          <tbody>
            {agents.map((host) => (
              <tr key={host.id}>
                <td>{host.id}</td>
                <td>{host.hostname}</td>
                <td>{host.os_name} {host.os_version}</td>
                <td>{host.architecture}</td>
                <td>{host.last_seen || 'Never'}</td>
              </tr>
            ))}
            {agents.length === 0 && (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center' }}>No agents registered</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HostInventory;
