import { ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import Card from '../../components/Card';

const ProducteurMessages = () => {
  const navigate = useNavigate();

  return (
    <div className="py-6">
      <button
        onClick={() => navigate('/producteur')}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-800 mb-6"
      >
        <ArrowLeft className="w-5 h-5" />
        Retour
      </button>

      <h2 className="text-2xl font-bold text-gray-800 mb-6">Mes Messages</h2>

      <Card>
        <div className="text-center py-12">
          <p className="text-gray-600">Aucun message pour le moment</p>
        </div>
      </Card>
    </div>
  );
};

export default ProducteurMessages;
