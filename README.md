# Application Django de Gestion d'Agenda CIM

Application web complète pour la gestion des réunions et événements de la CIM avec calendrier interactif FullCalendar et notifications par email.

## 📋 Fonctionnalités

- ✅ **Calendrier interactif** avec FullCalendar (Vue mois/semaine/jour)
- ✅ **Gestion des réunions** (Créer, modifier, supprimer)
- ✅ **Gestion des participants** avec informations complètes
- ✅ **Notifications email automatiques** via Gmail SMTP
- ✅ **Interface moderne** avec design responsive (Bleu, Blanc, Marron)
- ✅ **Interface d'administration** Django
- ✅ **Base de données SQLite3** (par défaut) ou PostgreSQL

## 🛠️ Technologies utilisées

- **Backend**: Django 5.0
- **Base de données**: SQLite3 (par défaut) / PostgreSQL (optionnel)
- **Frontend**: Bootstrap 5, FullCalendar 6
- **Email**: Gmail SMTP
- **Langues**: Python, JavaScript, HTML, CSS

## 📦 Installation

### Prérequis

1. Python 3.10 ou supérieur
2. Un compte Gmail avec mot de passe d'application (optionnel, pour les notifications email)
3. PostgreSQL (optionnel, si vous préférez PostgreSQL à SQLite3)

### Étapes d'installation

#### Option A: Installation avec SQLite3 (recommandé pour débuter)

1. **Cloner ou télécharger le projet**

2. **Exécuter le script de setup**
   ```bash
   setup.bat
   ```

3. **Passer à SQLite3** (supprime PostgreSQL)
   ```bash
   switch_to_sqlite.bat
   ```

4. **Configurer le fichier .env** (optionnel)
   - Ouvrir le fichier `.env`
   - Remplir uniquement si vous voulez les emails:
     - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (Gmail)
   - Pour SQLite3, assurez-vous que DB_ENGINE n'est **PAS** défini

5. **Créer un superutilisateur**
   ```bash
   venv\Scripts\activate
   python manage.py createsuperuser
   ```

6. **Lancer le serveur**
   ```bash
   run_server.bat
   ```

#### Option B: Installation avec PostgreSQL

1. **Cloner ou télécharger le projet**

2. **Créer la base de données PostgreSQL**
   ```bash
   createdb agenda_cim
   ```

3. **Exécuter le script de setup**
   ```bash
   setup.bat
   ```

4. **Configurer le fichier .env**
   - Ouvrir le fichier `.env`
   - Décommenter et remplir les informations PostgreSQL:
     - DB_ENGINE=django.db.backends.postgresql
     - DB_NAME, DB_USER, DB_PASSWORD (PostgreSQL)
     - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (Gmail)

5. **Installer psycopg2** (pour PostgreSQL)
   ```bash
   venv\Scripts\activate
   pip install psycopg2-binary
   ```

6. **Créer la base de données**
   ```bash
   python manage.py migrate
   ```

7. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```

8. **Lancer le serveur**
   ```bash
   run_server.bat
   ```

7. **Accéder à l'application**
   - Application: http://localhost:8000
   - Admin: http://localhost:8000/admin

## 📧 Configuration Email Gmail

Pour utiliser les notifications par email:

1. Connectez-vous à votre compte Gmail
2. Activez la validation en 2 étapes
3. Générez un "Mot de passe d'application":
   - Compte Google > Sécurité > Validation en 2 étapes
   - Mots de passe des applications
   - Sélectionnez "Autre" et nommez-le "CIM Agenda"
4. Copiez le mot de passe généré dans `.env` (EMAIL_HOST_PASSWORD)

## 🎨 Design

L'application utilise une palette de couleurs:
- **Bleu**: #1e40af (foncé), #3b82f6 (primaire)
- **Blanc**: #ffffff
- **Marron**: #6b5b47 (foncé), #8b7355 (clair)

## 📖 Utilisation

### Ajouter des participants

1. Aller dans "Participants"
2. Cliquer sur "Ajouter un participant"
3. Remplir le formulaire (Nom, Prénom, Email, etc.)

### Créer une réunion

1. Cliquer sur une date dans le calendrier ou "Nouvelle réunion"
2. Remplir les informations (Titre, Date, Heure, Lieu)
3. Sélectionner les participants
4. Enregistrer

Les participants recevront automatiquement une notification par email.

### Modifier/Supprimer une réunion

1. Cliquer sur une réunion dans le calendrier
2. Utiliser les boutons "Modifier" ou "Supprimer"

## 🔐 Accès Admin

L'interface d'administration Django est accessible à `/admin/` avec les identifiants du superutilisateur.

## 📁 Structure du projet

```
AGneda CIM/
├── agenda_cim/          # Configuration du projet
│   ├── settings.py      # Paramètres Django
│   └── urls.py          # URLs principales
├── meetings/            # Application réunions
│   ├── models.py        # Modèles (Meeting, Participant)
│   ├── views.py         # Vues
│   ├── forms.py         # Formulaires
│   └── admin.py         # Admin Django
├── templates/           # Templates HTML
│   ├── base.html
│   ├── meetings/        # Templates réunions
│   └── emails/          # Templates emails
├── static/              # Fichiers statiques
│   ├── css/             # Styles CSS
│   └── js/              # JavaScript
├── requirements.txt     # Dépendances Python
├── .env.example         # Exemple de configuration
├── setup.bat           # Script d'installation
└── run_server.bat      # Script de lancement
```

## 🆘 Dépannage

### Erreur de base de données

**SQLite3:**
- Vérifier que `db.sqlite3` est créé dans le répertoire du projet
- Assurez-vous que DB_ENGINE n'est PAS défini dans `.env`
- Exécutez `python manage.py migrate` si nécessaire

**PostgreSQL:**
- Vérifier que PostgreSQL est démarré
- Vérifier les credentials dans `.env`
- Vérifier que la base de données existe
- Assurez-vous que DB_ENGINE=django.db.backends.postgresql dans `.env`

### Emails non envoyés
- Vérifier EMAIL_HOST_USER et EMAIL_HOST_PASSWORD dans `.env`
- Utiliser un mot de passe d'application Gmail (pas le mot de passe du compte)
- Vérifier que la validation en 2 étapes est activée

### Erreur "Module not found"
- Activer l'environnement virtuel: `venv\Scripts\activate`
- Installer les dépendances: `pip install -r requirements.txt`

## 📝 Licence

© 2025 CIM - Tous droits réservés

## 👨‍💻 Support

Pour toute question ou problème, contactez l'administrateur système.
