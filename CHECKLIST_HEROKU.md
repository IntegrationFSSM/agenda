# 🚀 Checklist de Déploiement Heroku

## ✅ Avant de commencer

- [ ] Compte Heroku créé : https://signup.heroku.com/
- [ ] Git installé : `git --version`
- [ ] Heroku CLI installé : `heroku --version`
- [ ] Connexion Heroku : `heroku login`

## 📦 Fichiers de configuration

- [x] **Procfile** créé ✅
- [x] **runtime.txt** créé ✅
- [x] **requirements.txt** mis à jour ✅
- [x] **settings.py** configuré pour Heroku ✅
- [x] **.gitignore** présent ✅

## 🎯 Étapes de déploiement

### 1. Initialiser Git

```bash
git init
git add .
git commit -m "Initial commit"
```

- [ ] Git initialisé
- [ ] Fichiers ajoutés et committés

### 2. Créer l'application Heroku

```bash
heroku create votre-nom-app
```

**Nom suggéré** : `agenda-cim-uca` ou `cim-meetings-app`

- [ ] Application Heroku créée
- [ ] Nom de l'app : _________________

### 3. Ajouter PostgreSQL

```bash
heroku addons:create heroku-postgresql:essential-0
```

- [ ] Base de données PostgreSQL ajoutée

### 4. Configurer les variables d'environnement

```bash
# SECRET_KEY (générez une nouvelle !)
heroku config:set SECRET_KEY="nouvelle-secret-key-production"

# DEBUG à False
heroku config:set DEBUG=False

# ALLOWED_HOSTS avec votre nom d'app
heroku config:set ALLOWED_HOSTS="votre-nom-app.herokuapp.com"

# Email (optionnel)
heroku config:set EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
heroku config:set EMAIL_HOST_USER="votre-email@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="votre-mot-de-passe-app"
heroku config:set DEFAULT_FROM_EMAIL="votre-email@gmail.com"
```

- [ ] SECRET_KEY configurée
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS configuré
- [ ] Email configuré (optionnel)

### 5. Déployer

```bash
git push heroku main
```

ou si branche master :
```bash
git push heroku master
```

- [ ] Code déployé sur Heroku

### 6. Migrations

```bash
heroku run python manage.py migrate
```

- [ ] Migrations exécutées

### 7. Créer un superutilisateur

```bash
heroku run python manage.py createsuperuser
```

**Identifiants** :
- Username : _________________
- Email : _________________
- Password : _________________

- [ ] Superutilisateur créé

### 8. Collecter les fichiers statiques

```bash
heroku run python manage.py collectstatic --noinput
```

- [ ] Fichiers statiques collectés

### 9. Ouvrir l'application

```bash
heroku open
```

- [ ] Application accessible en ligne

## 🧪 Vérifications

- [ ] Page d'accueil s'affiche correctement
- [ ] CSS/JavaScript chargés (pas d'erreur 404)
- [ ] Page admin accessible : `/admin/`
- [ ] Connexion admin fonctionne
- [ ] Calendrier s'affiche
- [ ] Création de réunion possible
- [ ] Emails envoyés (si configuré)

## 🔧 Commandes de dépannage

### Voir les logs
```bash
heroku logs --tail
```

### Redémarrer l'app
```bash
heroku restart
```

### Voir les variables
```bash
heroku config
```

### Shell Django
```bash
heroku run python manage.py shell
```

## 📝 Informations importantes

**URL de l'application** : https://_________________.herokuapp.com  
**URL admin** : https://_________________.herokuapp.com/admin/  
**Nom de l'app Heroku** : _________________  

**Variables d'environnement configurées** :
- [ ] DATABASE_URL (automatique)
- [ ] SECRET_KEY
- [ ] DEBUG
- [ ] ALLOWED_HOSTS
- [ ] EMAIL_BACKEND
- [ ] EMAIL_HOST_USER
- [ ] EMAIL_HOST_PASSWORD

## 🔄 Pour mettre à jour

```bash
git add .
git commit -m "Description des modifications"
git push heroku main
heroku run python manage.py migrate  # Si models modifiés
heroku restart
```

## 🎉 Déploiement réussi !

- [ ] Application en ligne
- [ ] Toutes les fonctionnalités testées
- [ ] Documentation à jour

---

**Date de déploiement** : _________________  
**Version** : _________________
