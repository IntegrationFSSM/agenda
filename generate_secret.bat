@echo off
echo ======================================
echo GENERATEUR DE CLE SECRETE DJANGO
echo ======================================
echo.

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Générer la clé secrète
python generate_secret_key.py

echo.
echo ======================================
echo IMPORTANT:
echo 1. Copiez la ligne SECRET_KEY ci-dessus
echo 2. Collez-la dans votre fichier .env
echo 3. Remplacez l'ancienne SECRET_KEY
echo ======================================
echo.
pause
