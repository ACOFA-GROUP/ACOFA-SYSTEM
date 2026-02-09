import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  MapPin,
  Sprout,
  Package,
  Camera,
  MessageSquare,
  Leaf,
} from 'lucide-react';

const Sidebar = ({ isMobileOpen, onClose }) => {
  const menuItems = [
    { path: '/agent', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/agent/producteurs', icon: Users, label: 'Producteurs' },
    { path: '/agent/parcelles', icon: MapPin, label: 'Parcelles' },
    { path: '/agent/cultures', icon: Sprout, label: 'Cultures' },
    { path: '/agent/recoltes', icon: Package, label: 'Récoltes' },
    { path: '/agent/photos', icon: Camera, label: 'Photos' },
    { path: '/agent/messages', icon: MessageSquare, label: 'Messages' },
  ];

  return (
    <>
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`fixed lg:static inset-y-0 left-0 z-50 w-64 bg-white border-r border-gray-200 transform transition-transform duration-300 ease-in-out ${
          isMobileOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="flex items-center gap-3 p-6 border-b border-gray-200">
          <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
            <Leaf className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="font-bold text-gray-800">ACOFA</h2>
            <p className="text-xs text-gray-500">AGROLINK</p>
          </div>
        </div>

        <nav className="p-4 space-y-1">
          {menuItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/agent'}
              onClick={onClose}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`
              }
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;
