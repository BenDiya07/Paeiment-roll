@echo off
REM =====================================================
REM SNEL Payroll - Script de démarrage Windows
REM =====================================================

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║   SNEL PAYROLL - DEMARRAGE DU SYSTEME             ║
echo ╚════════════════════════════════════════════════════╝
echo.

REM Vérifier si MySQL est accessible
echo [1/3] Vérification de MySQL...
mysql -u snel_user -pmotdepasse -e "SELECT 1" > nul 2>&1
if errorlevel 1 (
    echo ⚠️  ATTENTION: MySQL n'est pas accessible
    echo Assurez-vous que:
    echo - Le serveur MySQL est en cours d'exécution
    echo - L'utilisateur 'snel_user' existe
    echo - Le mot de passe est 'motdepasse'
    echo.
    pause
) else (
    echo ✅ MySQL est accessible
)

echo.
echo [2/3] Démarrage du backend Flask...
echo Vous devez ouvrir un nouveau terminal pour cela.
echo.
echo Exécutez dans un nouveau CMD:
echo.
echo   cd f:\CODING\All\Paeiment-roll-1\snel-backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo Le backend démarrera sur http://localhost:5000
echo.

echo [3/3] Démarrage du serveur HTTP pour le frontend...
cd /d "f:\CODING\All\Paeiment-roll-1\all\snel-payroll-dashboard"

if exist "python.exe" (
    python -m http.server 8000
) else (
    REM Chercher Python dans le PATH
    for /f "delims=" %%i in ('where python') do set PYTHON=%%i
    if defined PYTHON (
        "%PYTHON%" -m http.server 8000
    ) else (
        echo ⚠️  ERREUR: Python n'est pas trouvé dans le PATH
        echo Assurez-vous que Python est installé et accessible
        pause
        exit /b 1
    )
)

echo.
echo ✅ Le serveur web démarre sur http://localhost:8000
echo.
echo Ouvrez http://localhost:8000 dans votre navigateur
echo.
pause
