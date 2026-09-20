# Guide de Déploiement Vercel — CamerAlert 🇨🇲

Ce document récapitule la configuration et les étapes pour déployer le projet **CamerAlert** sur **Vercel**.

---

## 1. Fichiers de configuration inclus

Le projet est configuré avec :
* **`vercel.json`** : Configuration des builds Vercel (`@vercel/python` pour le WSGI Django et `@vercel/static-build` pour les fichiers statiques).
* **`build_files.sh`** : Script d'installation des dépendances et de collecte des statiques (`collectstatic`).
* **`api/index.py`** & **`cameralert/wsgi.py`** : Points d'entrée WSGI Serverless compatibles Vercel (`app = application`).
* **`.python-version`** : Spécifie Python `3.12`.
* **`.vercelignore`** : Évite d'uploader les environnements virtuels locaux, caches et base SQLite locale.

---

## 2. Variables d'Environnement à Configurer sur Vercel

Dans le tableau de bord de votre projet Vercel (**Settings > Environment Variables**), ajoutez les variables suivantes :

### A. Sécurité & Django Core
| Variable | Valeur recommandée | Description |
| :--- | :--- | :--- |
| `SECRET_KEY` | *(Générer une clé aléatoire)* | Clé secrète de production Django |
| `DEBUG` | `False` | Désactive le mode debug en production |
| `ALLOWED_HOSTS` | `*` ou `.vercel.app,votre-domaine.cm` | Hôtes autorisés |
| `CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` | Domaines autorisés pour le CSRF |

### B. Base de Données (PostgreSQL)
> ⚠️ **Important :** Vercel Serverless dispose d'un système de fichiers éphémère et en lecture seule. SQLite local ne conserve pas les données. Il est fortement recommandé d'utiliser une base PostgreSQL gratuite (par exemple sur **[Neon.tech](https://neon.tech)**, **[Supabase](https://supabase.com)** ou **Vercel Postgres**).

| Variable | Exemple de valeur | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgres://user:password@ep-xyz.neon.tech/neondb?sslmode=require` | URL de connexion PostgreSQL |

### C. Stockage des Photos (Cloudinary)
> Les signalements incluent des photos de personnes disparues. Pour que ces photos persistent entre les requêtes serverless, configurez votre compte gratuit Cloudinary.

| Variable | Description |
| :--- | :--- |
| `CLOUDINARY_CLOUD_NAME` | Votre Cloud Name Cloudinary |
| `CLOUDINARY_API_KEY` | Votre Clé API Cloudinary |
| `CLOUDINARY_API_SECRET` | Votre Clé Secrète Cloudinary |

### D. Envoi d'Emails (Optionnel pour notifications et réinitialisation mot de passe)
| Variable | Exemple |
| :--- | :--- |
| `EMAIL_HOST` | `smtp.gmail.com` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `EMAIL_HOST_USER` | `contact@cameralert.cm` |
| `EMAIL_HOST_PASSWORD` | *(Mot de passe d'application Gmail)* |
| `DEFAULT_FROM_EMAIL` | `CamerAlert <contact@cameralert.cm>` |

---

## 3. Étapes de Déploiement

### Option 1 : Via l'interface Web Vercel (Recommandé)
1. Rendez-vous sur **[vercel.com](https://vercel.com)** et connectez-vous.
2. Cliquez sur **"Add New..." > "Project"**.
3. Importez votre dépôt GitHub **`hakimi-yvon/cameralert`**.
4. Dans **Environment Variables**, renseignez les variables listées ci-dessus (au minimum `SECRET_KEY`, `DEBUG=False`, et `DATABASE_URL`).
5. Cliquez sur **"Deploy"**.

### Option 2 : Via la CLI Vercel
```bash
npm install -g vercel
vercel login
vercel
```

---

## 4. Appliquer les Migrations sur la Base Distante

Une fois votre base PostgreSQL créée (par exemple sur Neon) et la variable `DATABASE_URL` configurée, appliquez les migrations depuis votre terminal local :

```bash
DATABASE_URL="postgres://..." .venv/bin/python manage.py migrate
```

Puis créez le compte administrateur :
```bash
DATABASE_URL="postgres://..." .venv/bin/python manage.py createsuperuser
```
