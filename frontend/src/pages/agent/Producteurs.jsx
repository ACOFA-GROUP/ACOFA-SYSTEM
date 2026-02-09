import { useEffect, useState } from 'react';
import { Plus, Search, Eye, Loader2 } from 'lucide-react';
import Card from '../../components/Card';
import api from '../../config/api';
import { useAuth } from '../../context/AuthContext';

const Producteurs = () => {
  const [producteurs, setProducteurs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const { user } = useAuth();

  const [formData, setFormData] = useState({
    nom_complet: '',
    sexe: 'M',
    age_approximatif: '',
    telephone: '',
    telephone_secondaire: '',
    village: '',
    localite: '',
    commune_cercle: '',
    region: '',
    latitude: '',
    longitude: '',
    cooperative_nom: '',
    langue_preferee: 'bambara',
  });

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchProducteurs();
  }, []);

  const fetchProducteurs = async () => {
    try {
      const response = await api.get('/api/v1/producteurs/');
      setProducteurs(response.data);
    } catch (error) {
      console.error('Erreur chargement producteurs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setSubmitting(true);

    try {
      const payload = {
        ...formData,
        age_approximatif: parseInt(formData.age_approximatif) || null,
        latitude: parseFloat(formData.latitude),
        longitude: parseFloat(formData.longitude),
        agent_enregistrement_id: user.user_id,
      };

      await api.post('/api/v1/producteurs/', payload);
      setSuccess('Producteur enregistré avec succès');
      setShowForm(false);
      fetchProducteurs();
      setFormData({
        nom_complet: '',
        sexe: 'M',
        age_approximatif: '',
        telephone: '',
        telephone_secondaire: '',
        village: '',
        localite: '',
        commune_cercle: '',
        region: '',
        latitude: '',
        longitude: '',
        cooperative_nom: '',
        langue_preferee: 'bambara',
      });
    } catch (error) {
      setError(error.response?.data?.detail || 'Erreur lors de l\'enregistrement');
    } finally {
      setSubmitting(false);
    }
  };

  const filteredProducteurs = producteurs.filter((p) =>
    p.nom_complet.toLowerCase().includes(searchTerm.toLowerCase()) ||
    p.telephone.includes(searchTerm) ||
    p.village?.toLowerCase().includes(searchTerm.toLowerCase())
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
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-gray-800">Producteurs</h2>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-secondary transition-colors"
        >
          <Plus className="w-5 h-5" />
          Ajouter producteur
        </button>
      </div>

      {success && (
        <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
          {success}
        </div>
      )}

      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
          {error}
        </div>
      )}

      {showForm && (
        <Card className="mb-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            Nouveau Producteur
          </h3>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nom complet *
                </label>
                <input
                  type="text"
                  value={formData.nom_complet}
                  onChange={(e) =>
                    setFormData({ ...formData, nom_complet: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Sexe *
                </label>
                <select
                  value={formData.sexe}
                  onChange={(e) =>
                    setFormData({ ...formData, sexe: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                >
                  <option value="M">Masculin</option>
                  <option value="F">Féminin</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Âge approximatif
                </label>
                <input
                  type="number"
                  value={formData.age_approximatif}
                  onChange={(e) =>
                    setFormData({ ...formData, age_approximatif: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Téléphone *
                </label>
                <input
                  type="tel"
                  value={formData.telephone}
                  onChange={(e) =>
                    setFormData({ ...formData, telephone: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Téléphone secondaire
                </label>
                <input
                  type="tel"
                  value={formData.telephone_secondaire}
                  onChange={(e) =>
                    setFormData({ ...formData, telephone_secondaire: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Village
                </label>
                <input
                  type="text"
                  value={formData.village}
                  onChange={(e) =>
                    setFormData({ ...formData, village: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Localité *
                </label>
                <input
                  type="text"
                  value={formData.localite}
                  onChange={(e) =>
                    setFormData({ ...formData, localite: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Commune/Cercle *
                </label>
                <input
                  type="text"
                  value={formData.commune_cercle}
                  onChange={(e) =>
                    setFormData({ ...formData, commune_cercle: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Région *
                </label>
                <input
                  type="text"
                  value={formData.region}
                  onChange={(e) =>
                    setFormData({ ...formData, region: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Latitude *
                </label>
                <input
                  type="number"
                  step="any"
                  value={formData.latitude}
                  onChange={(e) =>
                    setFormData({ ...formData, latitude: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Longitude *
                </label>
                <input
                  type="number"
                  step="any"
                  value={formData.longitude}
                  onChange={(e) =>
                    setFormData({ ...formData, longitude: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Coopérative
                </label>
                <input
                  type="text"
                  value={formData.cooperative_nom}
                  onChange={(e) =>
                    setFormData({ ...formData, cooperative_nom: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Langue préférée
                </label>
                <select
                  value={formData.langue_preferee}
                  onChange={(e) =>
                    setFormData({ ...formData, langue_preferee: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                >
                  <option value="bambara">Bambara</option>
                  <option value="francais">Français</option>
                  <option value="autres">Autres</option>
                </select>
              </div>
            </div>

            <div className="flex gap-4">
              <button
                type="submit"
                disabled={submitting}
                className="flex items-center gap-2 bg-primary text-white px-6 py-2 rounded-lg hover:bg-secondary transition-colors disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Enregistrement...
                  </>
                ) : (
                  'Enregistrer'
                )}
              </button>
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Annuler
              </button>
            </div>
          </form>
        </Card>
      )}

      <Card>
        <div className="mb-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Rechercher par nom, téléphone ou village..."
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
                  Nom
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Téléphone
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Village
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Région
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Date
                </th>
                <th className="text-left py-3 px-4 font-medium text-gray-700">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredProducteurs.map((producteur) => (
                <tr key={producteur.id} className="border-b border-gray-100">
                  <td className="py-3 px-4">{producteur.nom_complet}</td>
                  <td className="py-3 px-4">{producteur.telephone}</td>
                  <td className="py-3 px-4">{producteur.village || '-'}</td>
                  <td className="py-3 px-4">{producteur.region}</td>
                  <td className="py-3 px-4">
                    {new Date(producteur.date_enregistrement).toLocaleDateString()}
                  </td>
                  <td className="py-3 px-4">
                    <button className="p-2 text-primary hover:bg-green-50 rounded-lg transition-colors">
                      <Eye className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {filteredProducteurs.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            Aucun producteur trouvé
          </div>
        )}
      </Card>
    </div>
  );
};

export default Producteurs;
