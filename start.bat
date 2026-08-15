@echo off
title Nyaa Desktop Client - Lanzador

:: Elevar a administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit
)

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

:: 5. Instalar Transmission y aria2 mediante winget
echo [+] Instalando Transmission y aria2 (si no estan instalados)...
winget install --id Transmission.Transmission -e --silent --accept-package-agreements
winget install --id aria2.aria2 -e --silent --accept-package-agreements

:: 6. Verificar que Transmission y aria2 estén disponibles
echo [+] Verificando instalacion...
where transmission-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] transmission-cli no encontrado. Asegurate de que Transmission este instalado.
) else (
    echo [+] transmission-cli OK.
)
where aria2c >nul 2>nul
if %errorlevel% neq 0 (
    echo [AVISO] aria2c no encontrado. Asegurate de que aria2 este instalado.
) else (
    echo [+] aria2c OK.
)

:: 7. Lanzar la aplicación en segundo plano
echo.
echo ===================================================
echo    Iniciando Nyaa Desktop Client...
echo ===================================================
echo.

start "" pythonw nyaadesk.py

timeout /t 2 >nul
