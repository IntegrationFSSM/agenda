# 🔥 Dépannage : Erreur de Timeout SMTP

## ❌ Erreur rencontrée

```
TimeoutError: [WinError 10060] A connection attempt failed because 
the connected party did not properly respond
```

## 🔍 Causes possibles

### 1️⃣ Email universitaire au lieu de Gmail

**PROBLÈME** : Vous utilisez `y.ennhili7364@uca.ac.ma` (email UCA)  
**SOLUTION** : Vous devez utiliser un email `@gmail.com` pour Gmail SMTP !

#### ✅ Étapes :

1. **Créez un compte Gmail** : https://gmail.com (si vous n'en avez pas)
2. **Activez la validation en 2 étapes** sur ce compte Gmail
3. **Générez un mot de passe d'application** pour ce compte
4. **Modifiez `.env`** avec l'email Gmail :

```env
EMAIL_HOST_USER=votre-nouveau-compte@gmail.com
EMAIL_HOST_PASSWORD=mot-de-passe-application-gmail
DEFAULT_FROM_EMAIL=votre-nouveau-compte@gmail.com
```

### 2️⃣ Pare-feu Windows bloque le port 587

#### ✅ Solution : Autoriser SMTP dans le pare-feu

**Méthode 1 : Désactiver temporairement le pare-feu (TEST)**

1. Ouvrez **Pare-feu Windows Defender**
2. Cliquez sur **Activer ou désactiver le Pare-feu Windows**
3. Désactivez-le pour les réseaux privés
4. Testez : `python test_email.py`
5. **Réactivez-le immédiatement après le test !**

**Méthode 2 : Créer une règle de pare-feu (PERMANENT)**

1. Ouvrez **Pare-feu Windows Defender avec sécurité avancée**
2. Cliquez sur **Règles de sortie** → **Nouvelle règle**
3. Type : **Port**
4. Protocole : **TCP**
5. Port : **587**
6. Action : **Autoriser la connexion**
7. Nom : "SMTP Gmail Django"

### 3️⃣ Antivirus bloque SMTP

Certains antivirus (Avast, AVG, Kaspersky) bloquent SMTP.

#### ✅ Solution :

1. Ouvrez votre antivirus
2. Cherchez "Protection email" ou "Bouclier web"
3. Désactivez temporairement
4. Testez l'envoi d'email
5. Réactivez ensuite

### 4️⃣ Réseau universitaire bloque SMTP

Beaucoup d'universités bloquent le port 587 pour éviter le spam.

#### ✅ Solutions alternatives :

**Option A : Utiliser le port 465 (SSL)**

Modifiez votre `.env` :

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_USE_TLS=False
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe
DEFAULT_FROM_EMAIL=votre-email@gmail.com
```

**IMPORTANT** : Vous devez aussi modifier `settings.py` :

```python
# Dans agenda_cim/settings.py, ligne 109
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)
# Ajoutez cette ligne après :
EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
```

**Option B : Utiliser un hotspot mobile**

1. Activez le partage de connexion sur votre téléphone
2. Connectez votre PC au hotspot
3. Testez l'envoi d'email
4. Si ça marche → c'est bien le réseau universitaire qui bloque

**Option C : Utiliser mode console (développement)**

Pour le développement, gardez le mode console :

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les emails s'afficheront dans le terminal Django.

### 5️⃣ VPN ou Proxy actif

Si vous utilisez un VPN :

1. Désactivez le VPN
2. Testez l'envoi d'email
3. Réactivez si nécessaire

## 🧪 Tests de diagnostic

### Test 1 : Vérifier la connexion au serveur SMTP

```bash
# Dans PowerShell
Test-NetConnection smtp.gmail.com -Port 587
```

Résultat attendu :
- `TcpTestSucceeded : True` → Connexion OK
- `TcpTestSucceeded : False` → Port bloqué

### Test 2 : Tester avec telnet

```bash
# Dans PowerShell (en tant qu'administrateur)
telnet smtp.gmail.com 587
```

Si ça se connecte → Le port est ouvert  
Si ça timeout → Le port est bloqué

### Test 3 : Ping le serveur

```bash
ping smtp.gmail.com
```

Si pas de réponse → Problème réseau

## 📝 Checklist de résolution

Essayez dans cet ordre :

- [ ] **1. Vérifier que vous utilisez un email @gmail.com**
- [ ] **2. Générer un mot de passe d'application Gmail**
- [ ] **3. Tester la connexion** : `Test-NetConnection smtp.gmail.com -Port 587`
- [ ] **4. Désactiver temporairement le pare-feu** et tester
- [ ] **5. Désactiver temporairement l'antivirus** et tester
- [ ] **6. Essayer le port 465 (SSL)** au lieu de 587 (TLS)
- [ ] **7. Tester avec un hotspot mobile** (pour vérifier si c'est le réseau)
- [ ] **8. Utiliser le mode console** pour le développement

## 💡 Solution rapide pour continuer le développement

Si vous ne pouvez pas résoudre le problème tout de suite, utilisez le **mode console** :

```env
# Dans .env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Les emails s'afficheront dans le terminal où `python manage.py runserver` tourne.

Vous pourrez configurer l'envoi réel plus tard ou lors du déploiement !

## 📞 Support

Si rien ne fonctionne :
1. Vérifiez que vous utilisez bien un compte Gmail
2. Testez avec un hotspot mobile
3. Contactez le support informatique de votre université pour savoir s'ils bloquent SMTP

---

**Note** : Pour votre projet universitaire, le mode console est parfaitement acceptable pour les démonstrations !
