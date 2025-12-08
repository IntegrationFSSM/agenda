# ✅ CHECKLIST : Configuration Email Gmail

## 📝 Ce que vous devez faire dans votre fichier .env

Ouvrez `.env` et ajoutez/modifiez ces 4 lignes :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-application-16-caracteres
DEFAULT_FROM_EMAIL=votre-email@gmail.com
```

## 🔑 Comment obtenir le mot de passe d'application

### Étape 1 : Aller sur votre compte Google
🔗 https://myaccount.google.com/

### Étape 2 : Activer la validation en 2 étapes
1. Cliquez sur **Sécurité** (menu de gauche)
2. Cherchez **Validation en 2 étapes**
3. Cliquez sur **Commencer**
4. Suivez les instructions

### Étape 3 : Créer un mot de passe d'application
1. Retournez dans **Sécurité**
2. Cherchez **Mots de passe des applications** (en bas)
3. Cliquez dessus
4. Sélectionnez **Autre (nom personnalisé)**
5. Tapez "CIM Agenda"
6. Cliquez sur **Générer**

### Étape 4 : Copier le mot de passe
- Google affiche un mot de passe de 16 caractères
- Exemple : `abcd efgh ijkl mnop`
- **Copiez-le SANS les espaces** : `abcdefghijklmnop`

### Étape 5 : Coller dans .env
```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

## ✅ Vérification rapide

Après avoir modifié `.env` :

1. **Arrêtez le serveur** : `CTRL+C`
2. **Relancez** : `python manage.py runserver`
3. **Testez** : `python test_email.py`

## 📧 Exemple complet de .env

```env
# Sécurité
SECRET_KEY=2)9#pwp@99h*teo-xmq#gm*3w4x+r71*imf1yc97qjck

# Email Gmail - MODIFIEZ AVEC VOS VRAIES INFOS !
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST_USER=mohammed.agendacim@gmail.com
EMAIL_HOST_PASSWORD=abcdefghijklmnop
DEFAULT_FROM_EMAIL=mohammed.agendacim@gmail.com

# Général
ALLOWED_HOSTS=localhost,127.0.0.1
```

## ⚠️ Important

- ✅ Utilisez votre **vraie** adresse Gmail
- ✅ Utilisez le **mot de passe d'application** (pas votre mot de passe Gmail normal)
- ✅ Copiez le mot de passe **SANS espaces**
- ✅ La validation en 2 étapes **doit être activée**

## 🧪 Tester l'envoi d'email

```bash
python test_email.py
```

Le script vous demandera votre email et enverra un email de test.

## 📚 Guides complets

- **GUIDE_CONFIGURATION_GMAIL.md** : Guide détaillé avec captures d'écran
- **test_email.py** : Script de test automatique

---

**C'est tout !** Une fois configuré, vos réunions enverront automatiquement des emails aux participants.
