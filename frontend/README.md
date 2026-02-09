# ACOFA AGROLINK - Frontend Application

Application web de gestion agricole pour la plateforme ACOFA AGROLINK.

## Description

ACOFA AGROLINK est une plateforme de gestion agricole permettant aux agents ACOFA de collecter et gérer les données agricoles, et aux producteurs de consulter leurs cultures et communiquer avec ACOFA.

## Technologies Utilisées

- React 18
- React Router v6
- Axios
- Tailwind CSS
- Lucide React (icônes)
- React Hook Form
- Vite

## Fonctionnalités

### Pour les Agents ACOFA

- Dashboard avec statistiques
- Gestion des producteurs
- Gestion des cultures
- Upload et galerie de photos
- Système de messagerie

### Pour les Producteurs

- Consultation des cultures
- Upload de photos hebdomadaires
- Messagerie avec ACOFA

## Installation

1. Cloner le repository
2. Installer les dépendances:

```bash
npm install
```

3. Créer un fichier `.env` avec l'URL de l'API:

```
VITE_API_URL=https://acofa-system-production-c024.up.railway.app
```

## Développement

Lancer le serveur de développement:

```bash
npm run dev
```

L'application sera accessible sur `http://localhost:5173`

## Build

Construire l'application pour la production:

```bash
npm run build
```

Les fichiers de production seront générés dans le dossier `dist/`

## Identifiants de Test

### Agent ACOFA
- Email: agent@acofa.com
- Password: password123

### Producteur
- Téléphone: +223 70 00 00 01
- Code PIN: 123456

## Structure du Projet

```
src/
├── components/         # Composants réutilisables
│   ├── AgentLayout.jsx
│   ├── ProducteurLayout.jsx
│   ├── Card.jsx
│   ├── Header.jsx
│   ├── Sidebar.jsx
│   ├── StatCard.jsx
│   └── ProtectedRoute.jsx
├── config/            # Configuration
│   └── api.js
├── context/           # Contextes React
│   └── AuthContext.jsx
├── pages/             # Pages de l'application
│   ├── Login.jsx
│   ├── agent/
│   │   ├── Dashboard.jsx
│   │   ├── Producteurs.jsx
│   │   ├── Cultures.jsx
│   │   ├── Photos.jsx
│   │   └── Messages.jsx
│   └── producteur/
│       ├── Dashboard.jsx
│       ├── Cultures.jsx
│       ├── Photos.jsx
│       └── Messages.jsx
├── App.jsx
├── main.jsx
└── index.css
```

## API Backend

L'application communique avec une API backend FastAPI déployée sur Railway.

URL: https://acofa-system-production-c024.up.railway.app

Documentation API: https://acofa-system-production-c024.up.railway.app/docs

## Déploiement

L'application peut être déployée sur n'importe quelle plateforme supportant les applications React statiques:

- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront

Assurez-vous de configurer la variable d'environnement `VITE_API_URL` sur votre plateforme de déploiement.
