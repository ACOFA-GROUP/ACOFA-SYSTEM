import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Leaf, Loader2 } from 'lucide-react';

const Login = () => {
  const [activeTab, setActiveTab] = useState('agent');
  const [agentForm, setAgentForm] = useState({ username: '', password: '' });
  const [producteurForm, setProducteurForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleAgentSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(agentForm, 'agent');

    if (result.success) {
      navigate('/agent');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleProducteurSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    const result = await login(producteurForm, 'producteur');

    if (result.success) {
      navigate('/producteur');
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary rounded-full mb-4">
            <Leaf className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-800">ACOFA AGROLINK</h1>
          <p className="text-gray-600 mt-2">Plateforme de gestion agricole</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('agent')}
              className={`flex-1 py-4 px-6 font-medium transition-colors ${
                activeTab === 'agent'
                  ? 'bg-primary text-white'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              Agent ACOFA
            </button>
            <button
              onClick={() => setActiveTab('producteur')}
              className={`flex-1 py-4 px-6 font-medium transition-colors ${
                activeTab === 'producteur'
                  ? 'bg-primary text-white'
                  : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
              }`}
            >
              Producteur
            </button>
          </div>

          <div className="p-6">
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                {error}
              </div>
            )}

            {activeTab === 'agent' ? (
              <form onSubmit={handleAgentSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email
                  </label>
                  <input
                    type="email"
                    value={agentForm.username}
                    onChange={(e) => setAgentForm({ ...agentForm, username: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="agent@acofa.com"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Mot de passe
                  </label>
                  <input
                    type="password"
                    value={agentForm.password}
                    onChange={(e) => setAgentForm({ ...agentForm, password: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="••••••••"
                    required
                  />
                </div>

                <div className="bg-blue-50 p-3 rounded-lg text-sm text-blue-800">
                  <p className="font-medium mb-1">Identifiants de test :</p>
                  <p>Email: agent@acofa.com</p>
                  <p>Password: password123</p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-primary text-white py-3 rounded-lg font-medium hover:bg-secondary transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Connexion...
                    </>
                  ) : (
                    'Se connecter'
                  )}
                </button>
              </form>
            ) : (
              <form onSubmit={handleProducteurSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Téléphone
                  </label>
                  <input
                    type="tel"
                    value={producteurForm.username}
                    onChange={(e) => setProducteurForm({ ...producteurForm, username: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="+223 70 00 00 01"
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Code PIN
                  </label>
                  <input
                    type="password"
                    value={producteurForm.password}
                    onChange={(e) => setProducteurForm({ ...producteurForm, password: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="123456"
                    maxLength="6"
                    required
                  />
                </div>

                <div className="bg-blue-50 p-3 rounded-lg text-sm text-blue-800">
                  <p className="font-medium mb-1">Identifiants de test :</p>
                  <p>Téléphone: +223 70 00 00 01</p>
                  <p>Code PIN: 123456</p>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-primary text-white py-3 rounded-lg font-medium hover:bg-secondary transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Connexion...
                    </>
                  ) : (
                    'Se connecter'
                  )}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
