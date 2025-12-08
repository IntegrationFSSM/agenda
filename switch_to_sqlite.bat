@echo off
echo ======================================
echo Passage a SQLite3
echo ======================================
echo.

REM Activer l'environnement virtuel
echo [1/5] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour requirements.txt
echo.
echo [2/5] Installation des dépendances...
pip install -r requirements.txt

REM Vérifier si le fichier .env existe
echo.
echo [3/5] Configuration du fichier .env...
if not exist .env (
    echo Creation du fichier .env...
    copy .env.example .env
    echo IMPORTANT: Veuillez modifier .env avec vos parametres
) else (
    echo Fichier .env existant trouve
    echo IMPORTANT: Assurez-vous que DB_ENGINE n'est pas defini ou est sur sqlite3
)

REM Supprimer l'ancienne base de données SQLite si elle existe
echo.
echo [4/5] Nettoyage de l'ancienne base de donnees SQLite...
if exist db.sqlite3 (
    del db.sqlite3
    echo Ancienne base de donnees supprimee
)

REM Créer les migrations et la nouvelle base de données
echo.
echo [5/5] Creation de la nouvelle base de donnees SQLite3...
python manage.py migrate

echo.
echo ======================================
echo Migration vers SQLite3 terminee!
echo ======================================
echo.
echo Pour demarrer le serveur, executez:
echo python manage.py runserver
echo.
pause
