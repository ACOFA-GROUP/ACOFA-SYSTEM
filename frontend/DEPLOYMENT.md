# Guide de Déploiement - ACOFA AGROLINK

## Prérequis

- Node.js 18+ installé
- Compte sur une plateforme de déploiement (Vercel, Netlify, etc.)
- URL du backend API configurée

## Déploiement sur Vercel

1. Créer un compte sur [Vercel](https://vercel.com)

2. Installer Vercel CLI:
```bash
npm install -g vercel
```

3. Se connecter:
```bash
vercel login
```

4. Déployer:
```bash
vercel
```

5. Configurer les variables d'environnement dans Vercel:
   - Aller sur le dashboard Vercel
   - Sélectionner votre projet
   - Aller dans Settings > Environment Variables
   - Ajouter: `VITE_API_URL` = `https://acofa-system-production-c024.up.railway.app`

6. Redéployer pour appliquer les variables:
```bash
vercel --prod
```

## Déploiement sur Netlify

1. Créer un compte sur [Netlify](https://netlify.com)

2. Installer Netlify CLI:
```bash
npm install -g netlify-cli
```

3. Build le projet:
```bash
npm run build
```

4. Déployer:
```bash
netlify deploy --prod --dir=dist
```

5. Configurer les variables d'environnement dans Netlify:
   - Aller sur le dashboard Netlify
   - Sélectionner votre site
   - Aller dans Site settings > Environment variables
   - Ajouter: `VITE_API_URL` = `https://acofa-system-production-c024.up.railway.app`

## Configuration des Variables d'Environnement

L'application nécessite une seule variable d'environnement:

```
VITE_API_URL=https://acofa-system-production-c024.up.railway.app
```

Cette variable pointe vers le backend API hébergé sur Railway.

## Vérification Post-Déploiement

Après le déploiement, vérifiez:

1. La page de login s'affiche correctement
2. Les identifiants de test fonctionnent:
   - Agent: agent@acofa.com / password123
   - Producteur: +223 70 00 00 01 / 123456
3. Les données se chargent depuis l'API
4. Les images et styles s'affichent correctement
5. Le responsive fonctionne sur mobile

## Troubleshooting

### L'API ne répond pas

Vérifiez que:
- La variable `VITE_API_URL` est correctement configurée
- Le backend Railway est en ligne
- Il n'y a pas de problèmes CORS

### Les styles Tailwind ne s'affichent pas

- Vérifiez que `tailwind.config.js` et `postcss.config.js` sont présents
- Rebuild l'application: `npm run build`

### Erreur 404 sur les routes

Pour Netlify, créez un fichier `public/_redirects`:
```
/*    /index.html   200
```

Pour Vercel, le fichier `vercel.json` devrait contenir:
```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

## Support

Pour toute question ou problème, contactez l'équipe ACOFA.
