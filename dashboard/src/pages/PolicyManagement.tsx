import React, { useEffect, useState } from 'react';
import './Pages.css';
import { listPolicies, createPolicy, deletePolicy } from '../api/sdk.gen';

const PolicyManagement: React.FC = () => {
  const [policies, setPolicies] = useState<any[]>([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    os_target: '',
    content_id: '',
    profile_id: ''
  });

  const fetchPolicies = async () => {
    try {
      const res = await listPolicies();
      if (res.data) setPolicies(res.data);
    } catch (err) {
      console.error("Failed to fetch policies", err);
    }
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createPolicy({ body: formData });
      setShowModal(false);
      setFormData({ name: '', os_target: '', content_id: '', profile_id: '' });
      fetchPolicies();
    } catch (err) {
      console.error("Failed to create policy", err);
      alert("Failed to create policy");
    }
  };

  const handleDelete = async (id: string) => {
    if (confirm("Are you sure you want to delete this policy?")) {
      try {
        await deletePolicy({ path: { policyId: id } });
        fetchPolicies();
      } catch (err) {
        console.error("Failed to delete policy", err);
        alert("Failed to delete policy");
      }
    }
  };

  return (
    <div className="page-wrapper">
      <div className="page-header">
        <h1>Policy Management</h1>
        <button className="primary-btn" onClick={() => setShowModal(true)}>Create Policy</button>
      </div>

      <div className="glass-panel table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Target OS</th>
              <th>SCAP Profile</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {policies.map((policy) => (
              <tr key={policy.id}>
                <td>{policy.id}</td>
                <td>{policy.name}</td>
                <td><span className="badge badge-info">{policy.os_target}</span></td>
                <td><code style={{fontSize: '0.85em', color: '#9ca3af'}}>{policy.profile_id}</code></td>
                <td>
                  <button className="text-btn text-danger" onClick={() => handleDelete(policy.id)}>Remove</button>
                </td>
              </tr>
            ))}
            {policies.length === 0 && (
              <tr>
                <td colSpan={5} style={{ textAlign: 'center' }}>No policies defined</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="modal-backdrop" style={{position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000}}>
          <div className="glass-panel" style={{padding: '24px', width: '400px', backgroundColor: '#1e293b'}}>
            <h2 style={{marginTop: 0}}>Create Policy</h2>
            <form onSubmit={handleCreate} style={{display: 'flex', flexDirection: 'column', gap: '16px'}}>
              <div>
                <label style={{display: 'block', marginBottom: '8px', color: '#9ca3af'}}>Name</label>
                <input required type="text" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #334155', backgroundColor: '#0f172a', color: 'white'}} />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '8px', color: '#9ca3af'}}>Target OS (e.g. Ubuntu)</label>
                <input required type="text" value={formData.os_target} onChange={(e) => setFormData({...formData, os_target: e.target.value})} style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #334155', backgroundColor: '#0f172a', color: 'white'}} />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '8px', color: '#9ca3af'}}>Content ID (e.g. ssg-ubuntu2204-ds.xml)</label>
                <input required type="text" value={formData.content_id} onChange={(e) => setFormData({...formData, content_id: e.target.value})} style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #334155', backgroundColor: '#0f172a', color: 'white'}} />
              </div>
              <div>
                <label style={{display: 'block', marginBottom: '8px', color: '#9ca3af'}}>Profile ID (e.g. xccdf_org.ssgproject.content_profile_standard)</label>
                <input required type="text" value={formData.profile_id} onChange={(e) => setFormData({...formData, profile_id: e.target.value})} style={{width: '100%', padding: '8px', borderRadius: '4px', border: '1px solid #334155', backgroundColor: '#0f172a', color: 'white'}} />
              </div>
              <div style={{display: 'flex', justifyContent: 'flex-end', gap: '12px', marginTop: '16px'}}>
                <button type="button" className="text-btn" onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" className="primary-btn">Save</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default PolicyManagement;
