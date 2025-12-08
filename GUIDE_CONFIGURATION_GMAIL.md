# 📧 GUIDE : Configuration Gmail pour l'envoi d'emails

## 🎯 Problème actuel

Votre application est configurée pour afficher les emails dans la **console** au lieu de les envoyer réellement via Gmail.

## ✅ SOLUTION COMPLÈTE

### Étape 1 : Obtenir un mot de passe d'application Gmail

#### 📋 Instructions étape par étape :

1. **Connexion à votre compte Gmail**
   - Allez sur : https://myaccount.google.com/
   - Connectez-vous avec votre compte Gmail

2. **Activer la validation en 2 étapes** (obligatoire)
   - Allez dans **Sécurité** → **Validation en 2 étapes**
   - Cliquez sur **Commencer**
   - Suivez les instructions pour activer la validation en 2 étapes
   - **IMPORTANT** : Vous devez d'abord activer ceci avant de pouvoir créer un mot de passe d'application !

3. **Créer un mot de passe d'application**
   - Retournez dans **Sécurité**
   - Cherchez **Mots de passe des applications** (en bas de la section "Validation en 2 étapes")
   - Si vous ne voyez pas cette option, assurez-vous que la validation en 2 étapes est activée
   - Cliquez sur **Mots de passe des applications**

4. **Générer le mot de passe**
   - Dans "Sélectionner l'application" : choisissez **Autre (nom personnalisé)**
   - Tapez : **"CIM Agenda"** ou **"Django App"**
   - Cliquez sur **Générer**

5. **Copier le mot de passe**
   - Google affichera un mot de passe de 16 caractères (ex: `abcd efgh ijkl mnop`)
   - **COPIEZ CE MOT DE PASSE** (sans les espaces)
   - **ATTENTION** : Vous ne pourrez plus le voir après avoir fermé cette fenêtre !

### Étape 2 : Configurer votre fichier .env

Ouvrez votre fichier `.env` et modifiez ces lignes :

```env
# Configuration Email Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=votre-email@gmail.com
```

#### ⚠️ Remplacez par vos vraies informations :

- `EMAIL_HOST_USER` : Votre adresse Gmail complète (ex: `mohammed@gmail.com`)
- `EMAIL_HOST_PASSWORD` : Le mot de passe d'application de 16 caractères (SANS espaces)
- `DEFAULT_FROM_EMAIL` : La même adresse Gmail

#### 📝 Exemple COMPLET d'un fichier .env :

```env
# Configuration de sécurité
SECRET_KEY=2)9#pwp@99h*teo-xmq#gm*3w4x+r71*imf1yc97qjck

# Configuration Email Gmail
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=mohammed.agendacim@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=mohammed.agendacim@gmail.com

# Configuration générale
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Étape 3 : Redémarrer le serveur Django

1. **Arrêtez le serveur** : Appuyez sur `CTRL+C` dans le terminal
2. **Relancez le serveur** :
   ```bash
   python manage.py runserver
   ```

## ✅ Vérification : Tester l'envoi d'emails

### Option 1 : Via l'interface web

1. Allez sur http://localhost:8000
2. Créez une nouvelle réunion
3. Ajoutez des participants avec des emails valides
4. Enregistrez la réunion
5. Les emails devraient être envoyés !

### Option 2 : Via le shell Django (test rapide)

```bash
# Activez l'environnement virtuel
venv\Scripts\activate

# Ouvrez le shell Django
python manage.py shell

# Testez l'envoi d'email
from django.core.mail import send_mail

send_mail(
    subject='Test Email CIM Agenda',
    message='Ceci est un email de test.',
    from_email='votre-email@gmail.com',
    recipient_list=['votre-email@gmail.com'],
    fail_silently=False,
)

# Si aucune erreur, l'email a été envoyé !
exit()
```

Vérifiez votre boîte de réception (et le dossier spam) !

## 🔧 Variables .env nécessaires pour Gmail

Voici toutes les variables à définir dans `.env` :

| Variable | Valeur | Description |
|----------|--------|-------------|
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | Active l'envoi réel via SMTP |
| `EMAIL_HOST_USER` | `votre-email@gmail.com` | Votre adresse Gmail |
| `EMAIL_HOST_PASSWORD` | `abcdefghijklmnop` | Mot de passe d'application (16 caractères) |
| `DEFAULT_FROM_EMAIL` | `votre-email@gmail.com` | Email expéditeur par défaut |

**Variables optionnelles** (déjà configurées dans settings.py) :
- `EMAIL_HOST` : `smtp.gmail.com` (par défaut)
- `EMAIL_PORT` : `587` (par défaut)
- `EMAIL_USE_TLS` : `True` (par défaut)

## 🆘 Dépannage

### ❌ Erreur : "Authentication failed"

**Solution** :
- Vérifiez que la validation en 2 étapes est activée
- Régénérez un nouveau mot de passe d'application
- Assurez-vous de copier le mot de passe SANS espaces

### ❌ Erreur : "SMTPAuthenticationError"

**Solution** :
- Vérifiez que `EMAIL_HOST_USER` et `EMAIL_HOST_PASSWORD` sont corrects
- Vérifiez qu'il n'y a pas d'espaces supplémentaires
- Essayez de vous connecter à Gmail dans un navigateur

### ❌ Emails dans le dossier spam

**Solution** :
- Normal pour les emails de test
- Marquez l'email comme "Non spam"
- Les prochains emails arriveront dans la boîte de réception

### ❌ Erreur : "SMTPServerDisconnected"

**Solution** :
- Vérifiez votre connexion Internet
- Vérifiez que le port 587 n'est pas bloqué par un pare-feu

### 🐛 Mode DEBUG : Voir les emails dans la console

Si vous voulez temporairement voir les emails dans la console au lieu de les envoyer :

```env
# Pour le développement/test
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les emails s'afficheront dans le terminal au lieu d'être envoyés.

## 📝 Résumé des étapes

1. ✅ Activer la validation en 2 étapes sur Gmail
2. ✅ Créer un mot de passe d'application
3. ✅ Copier le mot de passe (16 caractères)
4. ✅ Modifier `.env` avec :
   - `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
   - `EMAIL_HOST_USER=votre-email@gmail.com`
   - `EMAIL_HOST_PASSWORD=votremotdepasse`
5. ✅ Redémarrer le serveur Django
6. ✅ Tester en créant une réunion

## 🔒 Sécurité

- ✅ Ne partagez JAMAIS votre mot de passe d'application
- ✅ Le fichier `.env` est déjà dans `.gitignore`
- ✅ Utilisez un email dédié pour l'application si possible
- ✅ Révoque les mots de passe d'application non utilisés

## 🎉 Envoi d'emails fonctionnel !

Une fois configuré, votre application pourra :
- ✅ Envoyer des notifications de réunion
- ✅ Notifier les participants par email
- ✅ Envoyer des rappels automatiques

---

**Besoin d'aide ?** Consultez la documentation Django : https://docs.djangoproject.com/en/5.0/topics/email/
