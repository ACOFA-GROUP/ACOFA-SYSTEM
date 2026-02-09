import { createContext, useContext, useState, useEffect } from 'react';
import api from '../config/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');

    if (storedUser && token) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = async (credentials, type) => {
    try {
      const endpoint = type === 'agent'
        ? '/api/v1/auth/agent/login'
        : '/api/v1/auth/producteur/login';

      const response = await api.post(endpoint, credentials);
      const { access_token, user_id, role, name } = response.data;

      localStorage.setItem('token', access_token);
      const userData = { user_id, role, name };
      localStorage.setItem('user', JSON.stringify(userData));
      setUser(userData);

      return { success: true, role };
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.detail || 'Échec de la connexion'
      };
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
