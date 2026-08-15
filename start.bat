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

:: Ocultar la ventana del lanzador
if not "%1"=="hide" (
    start "" "%~f0" hide
    exit
)

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
    timeout /t 5 >nul
    exit
)

:: 2. Actualizar pip
echo [+] Actualizando pip...
python -m pip install --upgrade pip --quiet >nul 2>&1

:: 3. Instalar dependencias requeridas
echo [+] Instalando dependencias...
pip install requests beautifulsoup4 pillow customtkinter --quiet >nul 2>&1

:: 4. Si existe requirements.txt, instalar tambien
if exist requirements.txt (
    echo [+] Instalando dependencias desde requirements.txt...
    pip install -r requirements.txt --quiet >nul 2>&1
)

:: 5. Instalar Transmission y aria2
echo [+] Verificando clientes BitTorrent...

:: Verificar e instalar Transmission
where transmission-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Instalando Transmission...
    winget install --id Transmission.Transmission -e --silent --accept-package-agreements >nul 2>&1
)

:: Verificar e instalar aria2
where aria2c >nul 2>nul
if %errorlevel% neq 0 (
    echo [+] Instalando aria2...
    winget install --id aria2.aria2 -e --silent --accept-package-agreements >nul 2>&1
)

:: 6. Detectar rutas exactas de los ejecutables
set "TRANSMISSION_FOUND=0"
for %%p in (
    "%ProgramFiles%\Transmission\transmission-cli.exe"
    "%ProgramFiles%\Transmission\bin\transmission-cli.exe"
    "%ProgramFiles(x86)%\Transmission\transmission-cli.exe"
    "%ProgramFiles(x86)%\Transmission\bin\transmission-cli.exe"
    "%LocalAppData%\Programs\Transmission\transmission-cli.exe"
    "%LocalAppData%\Programs\Transmission\bin\transmission-cli.exe"
    "%USERPROFILE%\scoop\shims\transmission-cli.exe"
) do (
    if exist %%p (
        set "TRANSMISSION_FOUND=1"
        set "TRANSMISSION_PATH=%%p"
        set "PATH=%%~dpp;%PATH%"
        goto :transmission_found
    )
)
:transmission_found

set "ARIA2_FOUND=0"
for %%p in (
    "%ProgramFiles%\aria2\aria2c.exe"
    "%ProgramFiles%\aria2\bin\aria2c.exe"
    "%ProgramFiles(x86)%\aria2\aria2c.exe"
    "%ProgramFiles(x86)%\aria2\bin\aria2c.exe"
    "%LocalAppData%\Programs\aria2\aria2c.exe"
    "%LocalAppData%\Programs\aria2\bin\aria2c.exe"
    "%LocalAppData%\Microsoft\WinGet\Links\aria2c.exe"
    "%USERPROFILE%\scoop\shims\aria2c.exe"
) do (
    if exist %%p (
        set "ARIA2_FOUND=1"
        set "ARIA2_PATH=%%p"
        set "PATH=%%~dpp;%PATH%"
        goto :aria2_found
    )
)
:aria2_found

:: 7. Iniciar aria2c en segundo plano (si existe)
if %ARIA2_FOUND%==1 (
    start /b "" "%ARIA2_PATH%" --daemon=true --enable-rpc --rpc-listen-port=6800 --rpc-allow-origin-all >nul 2>&1
)

:: 8. Verificar que nyaadesk.py existe
if not exist nyaadesk.py (
    echo [ERROR] No se encuentra nyaadesk.py
    timeout /t 3 >nul
    exit
)

:: 9. Lanzar la aplicación en segundo plano y cerrar el lanzador
echo.
echo Iniciando Nyaa Desktop Client...
echo.

:: Usar pythonw (sin ventana de consola)
start "" pythonw nyaadesk.py

:: Esperar 2 segundos para que la app se inicie
timeout /t 2 >nul

:: Salir silenciosamente
exit
