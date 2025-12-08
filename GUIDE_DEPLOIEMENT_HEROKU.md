# 🚀 Guide de Déploiement Heroku - AGneda CIM

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir :

- ✅ Un compte Heroku (gratuit) : https://signup.heroku.com/
- ✅ Git installé sur votre ordinateur
- ✅ Heroku CLI installé : https://devcenter.heroku.com/articles/heroku-cli

## 🔧 Installation de Heroku CLI

### Windows

Téléchargez et installez : https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli

Ou avec Chocolatey :
```bash
choco install heroku-cli
```

Vérifiez l'installation :
```bash
heroku --version
```

## 📦 Préparation du projet (DÉJÀ FAIT ✅)

Les fichiers suivants ont été créés automatiquement :

- ✅ **Procfile** : Indique comment démarrer l'application
- ✅ **runtime.txt** : Spécifie la version de Python
- ✅ **requirements.txt** : Mis à jour avec les dépendances Heroku
- ✅ **settings.py** : Configuré pour Heroku avec WhiteNoise et PostgreSQL

## 🚀 Étapes de déploiement

### Étape 1 : Initialiser Git (si pas encore fait)

```bash
# Dans le terminal (à la racine du projet)
git init
git add .
git commit -m "Initial commit - AGneda CIM"
```

### Étape 2 : Se connecter à Heroku

```bash
heroku login
```

Une fenêtre de navigateur s'ouvrira pour vous connecter.

### Étape 3 : Créer l'application Heroku

```bash
# Remplacez "agenda-cim-app" par le nom que vous voulez
heroku create agenda-cim-app
```

**Note** : Le nom doit être unique sur Heroku. Si déjà pris, essayez :
- `agenda-cim-uca`
- `cim-meetings-app`
- `agenda-cim-2025`

### Étape 4 : Ajouter une base de données PostgreSQL

```bash
heroku addons:create heroku-postgresql:essential-0
```

**Important** : Le plan `essential-0` est gratuit mais limité. Pour un usage plus important, utilisez un plan payant.

### Étape 5 : Configurer les variables d'environnement

```bash
# SECRET_KEY (générez-en une nouvelle pour la production)
heroku config:set SECRET_KEY="2)9#pwp@99h*teo-xmq#gm*3w4x+r71*imf1yc97qjck"

# DEBUG (TOUJOURS False en production)
heroku config:set DEBUG=False

# ALLOWED_HOSTS (remplacez par votre nom d'app)
heroku config:set ALLOWED_HOSTS="agenda-cim-app.herokuapp.com"

# Configuration Email (optionnel)
heroku config:set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
heroku config:set EMAIL_HOST_USER="votre-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="votre-mot-de-passe-application"
heroku config:set DEFAULT_FROM_EMAIL="votre-email@gmail.com"
```

**Note** : La variable `DATABASE_URL` est automatiquement configurée par Heroku PostgreSQL.

### Étape 6 : Déployer sur Heroku

```bash
git push heroku main
```

Si votre branche s'appelle `master` au lieu de `main` :
```bash
git push heroku master
```

### Étape 7 : Exécuter les migrations

```bash
heroku run python manage.py migrate
```

### Étape 8 : Créer un superutilisateur

```bash
heroku run python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte administrateur.

### Étape 9 : Collecter les fichiers statiques

```bash
heroku run python manage.py collectstatic --noinput
```

### Étape 10 : Ouvrir l'application

```bash
heroku open
```

Ou visitez : `https://votre-nom-app.herokuapp.com`

## 🎉 Votre application est en ligne !

Accédez à :
- **Application** : https://votre-nom-app.herokuapp.com/
- **Admin** : https://votre-nom-app.herokuapp.com/admin/

## 📝 Commandes utiles Heroku

### Voir les logs en temps réel
```bash
heroku logs --tail
```

### Redémarrer l'application
```bash
heroku restart
```

### Voir les variables d'environnement
```bash
heroku config
```

### Ajouter une variable d'environnement
```bash
heroku config:set NOM_VARIABLE="valeur"
```

### Supprimer une variable
```bash
heroku config:unset NOM_VARIABLE
```

### Ouvrir le shell Django sur Heroku
```bash
heroku run python manage.py shell
```

### Ouvrir la base de données PostgreSQL
```bash
heroku pg:psql
```

## 🔄 Mise à jour de l'application

Après avoir modifié votre code :

```bash
# 1. Commiter les changements
git add .
git commit -m "Description des modifications"

# 2. Déployer
git push heroku main

# 3. Si vous avez modifié les models, migrer
heroku run python manage.py migrate

# 4. Si nécessaire, collecter les fichiers statiques
heroku run python manage.py collectstatic --noinput
```

## 🐛 Dépannage

### Erreur : Application error / 500

Vérifiez les logs :
```bash
heroku logs --tail
```

### Erreur : Static files ne se chargent pas

```bash
heroku run python manage.py collectstatic --noinput
heroku restart
```

### Erreur : Database connection

Vérifiez que PostgreSQL est bien ajouté :
```bash
heroku addons
```

Si absent :
```bash
heroku addons:create heroku-postgresql:essential-0
```

### Erreur : DEBUG=True en production

**JAMAIS en production !**
```bash
heroku config:set DEBUG=False
```

### Voir toutes les configurations
```bash
heroku config
```

Doit afficher :
- DATABASE_URL
- SECRET_KEY
- DEBUG=False
- ALLOWED_HOSTS=votre-app.herokuapp.com

## 📊 Tableau de bord Heroku

Gérez votre application via le dashboard web :
https://dashboard.heroku.com/apps/votre-nom-app

Vous pouvez :
- Voir les métriques
- Gérer la base de données
- Voir les logs
- Configurer les variables d'environnement
- Gérer les add-ons

## 💰 Coûts

- **Heroku App** : Gratuit (avec limitations)
- **PostgreSQL Essential-0** : Gratuit (max 10,000 lignes)
- **Dyno gratuit** : Dort après 30 min d'inactivité

Pour plus de performances, passez aux plans payants :
```bash
heroku ps:resize web=basic
heroku addons:create heroku-postgresql:mini
```

## 🔒 Sécurité

### Checklist de sécurité :

- ✅ `DEBUG=False` en production
- ✅ `SECRET_KEY` différente de celle de développement
- ✅ `ALLOWED_HOSTS` configuré avec votre domaine
- ✅ Fichier `.env` dans `.gitignore`
- ✅ Utiliser HTTPS (automatique sur Heroku)
- ✅ Mots de passe forts pour le superutilisateur

## 📚 Ressources

- Documentation Heroku Django : https://devcenter.heroku.com/articles/django-app-configuration
- Documentation WhiteNoise : http://whitenoise.evans.io/
- Heroku CLI : https://devcenter.heroku.com/articles/heroku-cli

## ✨ Félicitations !

Votre application Django AGneda CIM est maintenant déployée sur Heroku ! 🎉

---

**Support** : En cas de problème, consultez les logs avec `heroku logs --tail`
