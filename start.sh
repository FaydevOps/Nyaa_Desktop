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

:: 5. Verificar/Instalar Chocolatey
set CHOCO_PATH=C:\ProgramData\chocolatey\bin\choco.exe
if exist "%CHOCO_PATH%" (
    echo [+] Chocolatey ya esta instalado.
    :: Agregar al PATH
    set "PATH=%PATH%;C:\ProgramData\chocolatey\bin"
) else (
    echo [+] Instalando Chocolatey...
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo instalar Chocolatey.
        pause
        exit
    )
    echo [+] Chocolatey instalado correctamente.
    :: Agregar al PATH
    set "PATH=%PATH%;C:\ProgramData\chocolatey\bin"
    :: Refrescar variables de entorno (opcional)
    call refreshenv >nul 2>&1
)

:: 6. Instalar Transmission y aria2 mediante Chocolatey
echo [+] Instalando Transmission y aria2 (si no estan instalados)...
choco install transmission aria2 -y --limit-output

:: 7. Verificar que Transmission y aria2 estén disponibles (añadir rutas si es necesario)
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

:: 8. Lanzar la aplicación en segundo plano
echo.
echo ===================================================
echo    Iniciando Nyaa Desktop Client...
echo ===================================================
echo.

:: Asegurar que el PATH incluye las rutas de los clientes antes de lanzar
start "" pythonw nyaadesk.py

timeout /t 2 >nul
