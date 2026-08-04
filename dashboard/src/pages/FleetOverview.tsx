import React, { useEffect, useState } from 'react';
import './Pages.css';
import { getComplianceOverview } from '../api/sdk.gen';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

const FleetOverview: React.FC = () => {
  const [data, setData] = useState<{ total: number, compliant: number, non_compliant: number, avg: number } | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await getComplianceOverview();
        if (res.data) {
          setData({
            total: res.data.total_agents,
            compliant: res.data.compliant_agents,
            non_compliant: res.data.non_compliant_agents,
            avg: res.data.average_score
          });
        }
      } catch (err) {
        console.error("Failed to fetch overview", err);
      }
    }
    fetchData();
  }, []);

  const chartData = [
    { name: 'Compliant', value: data?.compliant || 0, color: '#10b981' },
    { name: 'Non-Compliant', value: data?.non_compliant || 0, color: '#ef4444' },
  ];

  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Fleet Overview</h1>
        <p className="text-muted">Real-time compliance visibility across your infrastructure</p>
      </div>
      
      <div className="metrics-grid">
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Total Agents</h3>
          <div className="metric-value">{data?.total ?? '-'}</div>
        </div>
        
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Average Compliance</h3>
          <div className="metric-value">{data ? `${data.avg.toFixed(1)}%` : '-'}</div>
        </div>
        
        <div className="metric-card glass-panel">
          <h3 className="text-muted">Failed / Non-Compliant</h3>
          <div className="metric-value text-danger">{data?.non_compliant ?? '-'}</div>
        </div>
      </div>

      <div className="dashboard-charts glass-panel" style={{ marginTop: '24px', padding: '24px', minHeight: '300px' }}>
        <h3>Compliance Trends</h3>
        <div style={{ height: '300px' }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default FleetOverview;
