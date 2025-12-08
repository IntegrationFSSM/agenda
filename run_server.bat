@echo off
echo ================================================
echo Demarrage du serveur Django CIM Agenda
echo ================================================
echo.

REM Activer l'environnement virtuel
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Erreur: L'environnement virtuel n'existe pas.
    echo Veuillez executer setup.bat d'abord.
    pause
    exit /b 1
)

REM Démarrer le serveur de développement
echo Demarrage du serveur sur http://localhost:8000
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.
python manage.py runserver 8000
