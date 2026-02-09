import { useState } from 'react';
import { ArrowLeft, Upload, Loader2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../../components/Card';
import api from '../../config/api';

const ProducteurPhotos = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [typePhoto, setTypePhoto] = useState('suivi_hebdo');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Veuillez sélectionner une photo');
      return;
    }

    setError('');
    setSuccess('');
    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('type_photo', typePhoto);

      await api.post('/api/v1/photos/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess('Photo envoyée avec succès');
      setFile(null);
      setTypePhoto('suivi_hebdo');
      e.target.reset();
    } catch (error) {
      setError(error.response?.data?.detail || 'Erreur lors de l\'envoi');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="py-6">
      <button
        onClick={() => navigate('/producteur')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        Retour
      </button>

      <h2 className="text-2xl font-bold text-gray-800 mb-6">Envoyer une Photo</h2>

      <Card>
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg">
            {error}
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg">
            {success}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Type de photo
            </label>
            <select
              value={typePhoto}
              onChange={(e) => setTypePhoto(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="suivi_hebdo">Suivi hebdomadaire</option>
              <option value="culture">Culture générale</option>
              <option value="autre">Autre</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sélectionner une photo
            </label>
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary transition-colors">
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={handleFileChange}
                className="hidden"
                id="photo-upload"
              />
              <label
                htmlFor="photo-upload"
                className="cursor-pointer flex flex-col items-center"
              >
                <Upload className="w-12 h-12 text-gray-400 mb-4" />
                <p className="text-gray-600 mb-2">
                  {file ? file.name : 'Cliquez pour sélectionner une photo'}
                </p>
                <p className="text-sm text-gray-500">
                  Formats acceptés: JPG, PNG
                </p>
              </label>
            </div>
          </div>

          <button
            type="submit"
            disabled={uploading || !file}
            className="w-full flex items-center justify-center gap-2 bg-primary text-white py-3 rounded-lg hover:bg-secondary transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {uploading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Envoi en cours...
              </>
            ) : (
              <>
                <Upload className="w-5 h-5" />
                Envoyer la photo
              </>
            )}
          </button>
        </form>
      </Card>
    </div>
  );
};

export default ProducteurPhotos;
