import { useEffect, useState } from 'react';
import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../../components/Card';
import api from '../../config/api';

const ProducteurCultures = () => {
  const [cultures, setCultures] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchCultures();
  }, []);

  const fetchCultures = async () => {
    try {
      const response = await api.get('/api/v1/cultures/mes-cultures');
      setCultures(response.data);
    } catch (error) {
      console.error('Erreur chargement cultures:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatutBadge = (statut) => {
    const badges = {
      semis: { class: 'bg-blue-100 text-blue-700', label: 'Semis' },
      croissance: { class: 'bg-green-100 text-green-700', label: 'Croissance' },
      recolte: { class: 'bg-orange-100 text-orange-700', label: 'Récolte' },
    };
    return badges[statut] || { class: 'bg-gray-100 text-gray-700', label: statut };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Chargement...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="py-6">
      <button
        onClick={() => navigate('/producteur')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        Retour
      </button>

      <h2 className="text-2xl font-bold text-gray-800 mb-6">Mes Cultures</h2>

      {cultures.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <p className="text-gray-600">Vous n'avez pas encore de culture enregistrée</p>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {cultures.map((culture) => {
            const badge = getStatutBadge(culture.statut);
            return (
              <Card key={culture.id}>
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-lg font-bold text-gray-800">
                    {culture.type_culture}
                  </h3>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${badge.class}`}>
                    {badge.label}
                  </span>
                </div>

                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Superficie:</span>
                    <span className="font-medium">{culture.superficie_hectares} ha</span>
                  </div>
                  {culture.date_semis && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Date de semis:</span>
                      <span className="font-medium">
                        {new Date(culture.date_semis).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                  {culture.date_recolte_prevue && (
                    <div className="flex justify-between">
                      <span className="text-gray-600">Récolte prévue:</span>
                      <span className="font-medium">
                        {new Date(culture.date_recolte_prevue).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default ProducteurCultures;
