import { useEffect, useState } from 'react';
import { Search } from 'lucide-react';
import Card from '../../components/Card';
import api from '../../config/api';

const Cultures = () => {
  const [cultures, setCultures] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    fetchCultures();
  }, []);

  const fetchCultures = async () => {
    try {
      const response = await api.get('/api/v1/cultures/');
      setCultures(response.data);
    } catch (error) {
      console.error('Erreur chargement cultures:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatutBadge = (statut) => {
    const badges = {
      semis: 'bg-blue-100 text-blue-700',
      croissance: 'bg-green-100 text-green-700',
      recolte: 'bg-orange-100 text-orange-700',
    };
    return badges[statut] || 'bg-gray-100 text-gray-700';
  };

  const filteredCultures = cultures.filter((c) =>
    c.type_culture?.toLowerCase().includes(searchTerm.toLowerCase())
  );

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
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Cultures</h2>

      <Card>
        <div className="mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher par type de culture..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Type Culture
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Superficie (ha)
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Date Semis
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Statut
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredCultures.map((culture) => (
                <tr key={culture.id} className="border-b border-gray-100">
                  <td className="py-3 px-4 font-medium">{culture.type_culture}</td>
                  <td className="py-3 px-4">{culture.superficie_hectares}</td>
                  <td className="py-3 px-4">
                    {culture.date_semis
                      ? new Date(culture.date_semis).toLocaleDateString()
                      : '-'}
                  </td>
                  <td className="py-3 px-4">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${getStatutBadge(
                        culture.statut
                      )}`}
                    >
                      {culture.statut}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredCultures.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            Aucune culture trouvée
          </div>
        )}
      </Card>
    </div>
  );
};

export default Cultures;
