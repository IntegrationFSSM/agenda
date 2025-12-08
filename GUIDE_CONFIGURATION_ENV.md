# 📝 GUIDE DE CONFIGURATION .env POUR SQLITE3

## ✅ Configuration MINIMALE pour SQLite3

Ouvrez votre fichier `.env` et assurez-vous qu'il contient **au minimum** :

```env
# Configuration de sécurité
SECRET_KEY=django-insecure-development-key-change-this-in-production-123456789
DEBUG=True

# Configuration générale
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🎯 C'EST TOUT ! SQLite3 fonctionne automatiquement

**IMPORTANT**: Pour utiliser SQLite3, vous n'avez PAS besoin de définir :
- ❌ DB_ENGINE
- ❌ DB_NAME
- ❌ DB_USER
- ❌ DB_PASSWORD
- ❌ DB_HOST
- ❌ DB_PORT

Si ces variables sont définies (non commentées), **commentez-les** avec `#` devant chaque ligne.

## 📧 Configuration Email (OPTIONNEL)

Si vous voulez activer les notifications par email plus tard :

```env
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-app-password-gmail
```

**Vous pouvez laisser vide pour l'instant** :

```env
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

## ✨ Exemple de fichier .env COMPLET pour SQLite3

Copiez ce contenu dans votre fichier `.env` :

```env
# Configuration de sécurité
SECRET_KEY=django-insecure-development-key-change-this-in-production-123456789
DEBUG=True

# Configuration de la base de données SQLite3
# SQLite3 est utilisé par défaut - RIEN À CONFIGURER !

# Configuration Email Gmail (optionnel)
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

# Configuration générale
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🔄 Pour PASSER À PostgreSQL plus tard

Ajoutez ces lignes (décommentées) dans votre `.env` :

```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=agenda_cim
DB_USER=postgres
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=5432
```

## 🚀 Vérification

Votre serveur Django devrait déjà fonctionner avec SQLite3 !

Vérifiez que le fichier `db.sqlite3` existe dans votre projet. Si oui, tout est bon ! ✅
