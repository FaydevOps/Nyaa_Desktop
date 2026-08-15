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

:: =============================================
:: INSTALACIÓN DE CLIENTES BITTORRENT (Windows)
:: =============================================

:: 5. Verificar/Instalar chocolatey (gestor de paquetes)
echo.
echo [+] Verificando chocolatey...
where choco >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] Chocolatey no encontrado. Instalando...
    "%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -ExecutionPolicy Bypass -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    if %errorlevel% neq 0 (
        echo [ERROR] No se pudo instalar chocolatey.
        echo Descargalo manualmente desde https://chocolatey.org/
        pause
        exit
    )
    echo [+] Chocolatey instalado correctamente.
) else (
    echo [+] Chocolatey ya esta instalado.
)

:: 6. Instalar aria2 (si no está instalado)
echo.
echo [+] Verificando aria2...
where aria2c >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] aria2 no encontrado. Instalando con chocolatey...
    choco install aria2 -y --limit-output
    if %errorlevel% neq 0 (
        echo [AVISO] No se pudo instalar aria2. La descarga automatica podria no funcionar.
    ) else (
        echo [+] aria2 instalado correctamente.
    )
) else (
    echo [+] aria2 ya esta instalado.
)

:: 7. Instalar transmission-cli (opcional, por si aria2 falla)
echo.
echo [+] Verificando transmission-cli...
where transmission-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [INFO] transmission-cli no encontrado. Instalando con chocolatey...
    choco install transmission-cli -y --limit-output
    if %errorlevel% neq 0 (
        echo [AVISO] No se pudo instalar transmission-cli. Solo se usara aria2 si esta disponible.
    ) else (
        echo [+] transmission-cli instalado correctamente.
    )
) else (
    echo [+] transmission-cli ya esta instalado.
)

:: =============================================
:: LANZAR LA APLICACIÓN
:: =============================================
echo.
echo ===================================================
echo    Iniciando Nyaa Desktop Client...
echo ===================================================
echo.

:: Comprobar que existe el archivo principal
if not exist "nyaa_desktop.py" (
    if not exist "nyaa_desktop_pro.py" (
        echo [ERROR] No se encuentra el archivo principal (nyaa_desktop.py o nyaa_desktop_pro.py).
        echo Asegurate de que el script este en esta carpeta.
        pause
        exit
    ) else (
        set SCRIPT=nyaa_desktop_pro.py
    )
) else (
    set SCRIPT=nyaa_desktop.py
)

:: Lanzar en segundo plano con pythonw (sin ventana de consola)
start "" pythonw "%SCRIPT%"

:: Pequeña pausa para que la ventana se cierre
timeout /t 2 >nul
