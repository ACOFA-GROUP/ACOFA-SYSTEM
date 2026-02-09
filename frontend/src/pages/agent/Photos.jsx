import { useEffect, useState } from 'react';
import { Upload } from 'lucide-react';
import Card from '../../components/Card';
import api from '../../config/api';

const Photos = () => {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPhotos();
  }, []);

  const fetchPhotos = async () => {
    try {
      const response = await api.get('/api/v1/photos/');
      setPhotos(response.data);
    } catch (error) {
      console.error('Erreur chargement photos:', error);
    } finally {
      setLoading(false);
    }
  };

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
        <h2 className="text-2xl font-bold text-gray-800">Photos</h2>
        <button className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg hover:bg-secondary transition-colors">
          <Upload className="w-5 h-5" />
          Upload Photo
        </button>
      </div>

      <Card>
        {photos.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600">Aucune photo disponible</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {photos.map((photo) => (
              <div key={photo.id} className="border rounded-lg overflow-hidden">
                <img
                  src={photo.url_photo}
                  alt={photo.type_photo}
                  className="w-full h-48 object-cover"
                />
                <div className="p-2">
                  <p className="text-xs text-gray-600">{photo.type_photo}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
};

export default Photos;
