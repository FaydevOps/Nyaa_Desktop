@echo off
title Nyaa Desktop Client - Lanzador

cd /d "%~dp0"

cls
echo ===================================================
echo    Verificando entorno e instalando dependencias
echo ===================================================
echo.

:: 1. Verificar Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python no esta instalado o no esta en el PATH.
    echo Instala Python desde python.org y vuelve a intentar.
    pause
    exit
)

:: 2. Actualizar pip
echo [+] Actualizando pip...
python -m pip install --upgrade pip --quiet

:: 3. Instalar dependencias requeridas
echo [+] Instalando requests, beautifulsoup4, pillow, customtkinter...
pip install requests beautifulsoup4 pillow customtkinter --quiet

:: 4. Si existe requirements.txt, instalar también
if exist requirements.txt (
    echo [+] Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt --quiet
) else (
    echo [AVISO] No se encontro requirements.txt. Omitiendo.
)

:: 5. Lanzar la aplicación en segundo plano
echo.
echo ===================================================
echo    Iniciando Nyaa Desktop Client...
echo ===================================================
echo.

start "" pythonw nyaadesk.py

timeout /t 2 >nul
exit
