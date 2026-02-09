import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sprout, Camera, MessageSquare } from 'lucide-react';
import Card from '../../components/Card';
import api from '../../config/api';

const ProducteurDashboard = () => {
  const navigate = useNavigate();
  const [stats, setStats] = useState({
    cultures: 0,
    messages: 0,
  });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const culturesRes = await api.get('/api/v1/cultures/mes-cultures');
        setStats({
          cultures: culturesRes.data.length,
          messages: 0,
        });
      } catch (error) {
        console.error('Erreur chargement stats:', error);
      }
    };

    fetchStats();
  }, []);

  const menuCards = [
    {
      title: 'Mes Cultures',
      description: `${stats.cultures} culture(s) enregistrée(s)`,
      icon: Sprout,
      color: 'bg-green-100',
      iconColor: 'text-primary',
      path: '/producteur/cultures',
    },
    {
      title: 'Envoyer Photo',
      description: 'Partagez des photos de vos cultures',
      icon: Camera,
      color: 'bg-blue-100',
      iconColor: 'text-blue-600',
      path: '/producteur/photos',
    },
    {
      title: 'Mes Messages',
      description: `${stats.messages} message(s)`,
      icon: MessageSquare,
      color: 'bg-orange-100',
      iconColor: 'text-orange-600',
      path: '/producteur/messages',
    },
  ];

  return (
    <div className="py-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">
        Bienvenue sur votre espace
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {menuCards.map((card) => (
          <Card
            key={card.path}
            onClick={() => navigate(card.path)}
            className="hover:scale-105 transition-transform"
          >
            <div className="flex flex-col items-center text-center">
              <div className={`p-4 rounded-full ${card.color} mb-4`}>
                <card.icon className={`w-8 h-8 ${card.iconColor}`} />
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">
                {card.title}
              </h3>
              <p className="text-gray-600">{card.description}</p>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default ProducteurDashboard;
