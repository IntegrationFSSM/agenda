@echo off
echo ================================================
echo Configuration de l'application CIM Agenda
echo ================================================
echo.

REM Créer un environnement virtuel
echo [1/6] Creation de l'environnement virtuel...
python -m venv venv
if %errorlevel% neq 0 (
    echo Erreur: Python n'est pas installe ou n'est pas dans le PATH
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
echo [2/6] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances
echo [3/6] Installation des dependances...
pip install --upgrade pip
pip install -r requirements.txt

REM Créer le fichier .env si il n'existe pas
if not exist .env (
    echo [4/6] Creation du fichier .env...
    copy .env.example .env
    echo.
    echo IMPORTANT: Veuillez editer le fichier .env avec vos informations:
    echo - SECRET_KEY
    echo - DB_NAME, DB_USER, DB_PASSWORD (PostgreSQL)
    echo - EMAIL_HOST_USER, EMAIL_HOST_PASSWORD (Gmail)
    echo.
    pause
) else (
    echo [4/6] Le fichier .env existe deja
)

REM Appliquer les migrations
echo [5/6] Application des migrations de base de donnees...
python manage.py makemigrations
python manage.py migrate

REM Créer les répertoires pour les fichiers statiques
echo [6/6] Creation des repertoires statiques...
if not exist staticfiles mkdir staticfiles
if not exist media mkdir media

echo.
echo ================================================
echo Configuration terminee avec succes!
echo ================================================
echo.
echo Prochaines etapes:
echo 1. Editez le fichier .env avec vos informations
echo 2. Assurez-vous que PostgreSQL est installe et en cours d'execution
echo 3. Creez la base de donnees PostgreSQL: createdb agenda_cim
echo 4. Creez un superuser: python manage.py createsuperuser
echo 5. Lancez le serveur: run_server.bat
echo.
pause
