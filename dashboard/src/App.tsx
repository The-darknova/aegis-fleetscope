
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import FleetOverview from './pages/FleetOverview';
import HostInventory from './pages/HostInventory';
import HistoricalReports from './pages/HistoricalReports';
import PolicyManagement from './pages/PolicyManagement';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<FleetOverview />} />
          <Route path="inventory" element={<HostInventory />} />
          <Route path="reports" element={<HistoricalReports />} />
          <Route path="policies" element={<PolicyManagement />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
