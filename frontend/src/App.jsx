import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AgentLayout from './components/AgentLayout';
import ProducteurLayout from './components/ProducteurLayout';

import Login from './pages/Login';

import AgentDashboard from './pages/agent/Dashboard';
import Producteurs from './pages/agent/Producteurs';
import Parcelles from './pages/agent/Parcelles';
import Cultures from './pages/agent/Cultures';
import Recoltes from './pages/agent/Recoltes';
import Photos from './pages/agent/Photos';
import Messages from './pages/agent/Messages';

import ProducteurDashboard from './pages/producteur/Dashboard';
import ProducteurCultures from './pages/producteur/Cultures';
import ProducteurPhotos from './pages/producteur/Photos';
import ProducteurMessages from './pages/producteur/Messages';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login />} />

          <Route
            path="/agent"
            element={
              <ProtectedRoute allowedRole="agent">
                <AgentLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<AgentDashboard />} />
            <Route path="producteurs" element={<Producteurs />} />
            <Route path="parcelles" element={<Parcelles />} />
            <Route path="cultures" element={<Cultures />} />
            <Route path="recoltes" element={<Recoltes />} />
            <Route path="photos" element={<Photos />} />
            <Route path="messages" element={<Messages />} />
          </Route>

          <Route
            path="/producteur"
            element={
              <ProtectedRoute allowedRole="producteur">
                <ProducteurLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<ProducteurDashboard />} />
            <Route path="cultures" element={<ProducteurCultures />} />
            <Route path="photos" element={<ProducteurPhotos />} />
            <Route path="messages" element={<ProducteurMessages />} />
          </Route>

          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
