import { useState } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Overview from './pages/Overview';
import Monitoring from './pages/Monitoring';
import TunnelMap from './pages/TunnelMap';
import Alerts from './pages/Alerts';import Hazards from './pages/Hazards';import Workers from './pages/Workers';import Inspections from './pages/Inspections';import Compliance from './pages/Compliance';import Reports from './pages/Reports';import Notifications from './pages/Notifications';import Settings from './pages/Settings';
export default function App(){ const [tick,setTick]=useState(0); const refresh=()=>setTick(v=>v+1); return <Layout onRefresh={refresh}><Routes><Route path="/" element={<Overview tick={tick} refresh={refresh}/>}/><Route path="/monitoring" element={<Monitoring/>}/><Route path="/map" element={<TunnelMap/>}/><Route path="/alerts" element={<Alerts/>}/><Route path="/hazards" element={<Hazards/>}/><Route path="/workers" element={<Workers/>}/><Route path="/inspections" element={<Inspections/>}/><Route path="/compliance" element={<Compliance/>}/><Route path="/reports" element={<Reports/>}/><Route path="/notifications" element={<Notifications/>}/><Route path="/settings" element={<Settings/>}/><Route path="*" element={<Navigate to="/" replace/>}/></Routes></Layout> }
