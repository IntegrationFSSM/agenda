@echo off
echo ======================================
echo DEPLOIEMENT HEROKU - AGneda CIM
echo ======================================
echo.

REM Vérifier si Git est installé
echo [1/8] Verification de Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Git n'est pas installe
    echo Installez Git: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo Git OK

REM Vérifier si Heroku CLI est installé
echo.
echo [2/8] Verification de Heroku CLI...
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Heroku CLI n'est pas installe
    echo Installez Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)
echo Heroku CLI OK

REM Initialiser Git si nécessaire
echo.
echo [3/8] Initialisation de Git...
if not exist .git (
    git init
    echo Git initialise
) else (
    echo Git deja initialise
)

REM Ajouter le fichier .gitignore si nécessaire
echo.
echo [4/8] Verification du .gitignore...
if exist .gitignore (
    echo .gitignore existe
) else (
    echo Creation du .gitignore...
    (
        echo .env
        echo *.pyc
        echo __pycache__/
        echo db.sqlite3
        echo staticfiles/
        echo media/
        echo .venv/
        echo venv/
        echo *.log
        echo .DS_Store
    ) > .gitignore
)

REM Commit des fichiers
echo.
echo [5/8] Commit des fichiers...
git add .
git commit -m "Preparation pour deploiement Heroku" 2>nul
if errorlevel 1 (
    echo Aucun changement a commiter ou deja commite
) else (
    echo Fichiers commites
)

REM Connexion à Heroku
echo.
echo [6/8] Connexion a Heroku...
echo IMPORTANT: Une fenetre de navigateur va s'ouvrir pour vous connecter
pause
heroku login

REM Demander le nom de l'application
echo.
echo [7/8] Creation de l'application Heroku...
set /p APP_NAME="Entrez le nom de votre application (ex: agenda-cim-app): "

REM Créer l'application
heroku create %APP_NAME%
if errorlevel 1 (
    echo.
    echo ERREUR: Impossible de creer l'application (nom peut-etre deja pris)
    echo Essayez un autre nom
    pause
    exit /b 1
)

REM Ajouter PostgreSQL
echo.
echo [8/8] Ajout de la base de donnees PostgreSQL...
heroku addons:create heroku-postgresql:essential-0 --app %APP_NAME%

echo.
echo ======================================
echo INITIALISATION TERMINEE !
echo ======================================
echo.
echo Prochaines etapes:
echo.
echo 1. Configurez les variables d'environnement:
echo    heroku config:set SECRET_KEY="votre-secret-key" --app %APP_NAME%
echo    heroku config:set DEBUG=False --app %APP_NAME%
echo    heroku config:set ALLOWED_HOSTS="%APP_NAME%.herokuapp.com" --app %APP_NAME%
echo.
echo 2. Deployez l'application:
echo    git push heroku main
echo.
echo 3. Executez les migrations:
echo    heroku run python manage.py migrate --app %APP_NAME%
echo.
echo 4. Creez un superutilisateur:
echo    heroku run python manage.py createsuperuser --app %APP_NAME%
echo.
echo 5. Ouvrez votre application:
echo    heroku open --app %APP_NAME%
echo.
echo Consultez GUIDE_DEPLOIEMENT_HEROKU.md pour plus de details
echo.
pause
