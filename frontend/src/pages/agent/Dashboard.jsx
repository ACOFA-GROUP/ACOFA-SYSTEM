import { useEffect, useState } from 'react';
import { Users, MapPin, Sprout, Package } from 'lucide-react';
import StatCard from '../../components/StatCard';
import api from '../../config/api';

const Dashboard = () => {
  const [stats, setStats] = useState({
    producteurs: 0,
    parcelles: 0,
    cultures: 0,
    recoltes: 0,
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const producteursRes = await api.get('/api/v1/producteurs/');
        const culturesRes = await api.get('/api/v1/cultures/');

        setStats({
          producteurs: producteursRes.data.length,
          parcelles: 0,
          cultures: culturesRes.data.length,
          recoltes: 0,
        });
      } catch (error) {
        console.error('Erreur chargement stats:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Tableau de bord</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={Users}
          title="Producteurs"
          value={stats.producteurs}
          color="primary"
        />
        <StatCard
          icon={MapPin}
          title="Parcelles"
          value={stats.parcelles}
          color="blue"
        />
        <StatCard
          icon={Sprout}
          title="Cultures"
          value={stats.cultures}
          color="primary"
        />
        <StatCard
          icon={Package}
          title="Récoltes"
          value={stats.recoltes}
          color="orange"
        />
      </div>
    </div>
  );
};

export default Dashboard;
