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

:: 5. Instalar Transmission y aria2 mediante winget (si no estan instalados)
echo [+] Instalando Transmission y aria2 (si no estan instalados)...

:: Verificar e instalar Transmission
where transmission-cli >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] Transmission no encontrado. Instalando...
    winget install --id Transmission.Transmission -e --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [ERROR] Fallo la instalacion de Transmission.
    )
) else (
    echo [+] Transmission ya esta instalado.
)

:: Verificar e instalar aria2
where aria2c >nul 2>nul
if %errorlevel% neq 0 (
    echo [!] aria2 no encontrado. Instalando...
    winget install --id aria2.aria2 -e --silent --accept-package-agreements
    if %errorlevel% neq 0 (
        echo [ERROR] Fallo la instalacion de aria2.
    )
) else (
    echo [+] aria2 ya esta instalado.
)

:: 6. Verificar nuevamente con rutas comunes de instalacion
echo.
echo [+] Verificando instalacion...

:: Buscar transmission-cli en rutas tipicas de Windows
set "TRANSMISSION_FOUND=0"
for %%p in (
    "%ProgramFiles%\Transmission\transmission-cli.exe"
    "%ProgramFiles(x86)%\Transmission\transmission-cli.exe"
    "%LocalAppData%\Programs\Transmission\transmission-cli.exe"
) do (
    if exist %%p (
        set "TRANSMISSION_FOUND=1"
        echo [+] transmission-cli encontrado en: %%p
        :: Agregar al PATH temporalmente
        set "PATH=%%~dpp;%PATH%"
    )
)

if %TRANSMISSION_FOUND%==0 (
    echo [AVISO] transmission-cli no encontrado. Asegurate de que Transmission este instalado.
    echo        Puedes descargarlo desde: https://transmissionbt.com/
) else (
    echo [+] transmission-cli OK.
)

:: Buscar aria2c en rutas tipicas de Windows
set "ARIA2_FOUND=0"
for %%p in (
    "%ProgramFiles%\aria2\aria2c.exe"
    "%ProgramFiles(x86)%\aria2\aria2c.exe"
    "%LocalAppData%\Programs\aria2\aria2c.exe"
    "%USERPROFILE%\scoop\apps\aria2\current\aria2c.exe"
) do (
    if exist %%p (
        set "ARIA2_FOUND=1"
        echo [+] aria2c encontrado en: %%p
        :: Agregar al PATH temporalmente
        set "PATH=%%~dpp;%PATH%"
    )
)

if %ARIA2_FOUND%==0 (
    echo [AVISO] aria2c no encontrado. Asegurate de que aria2 este instalado.
    echo        Puedes descargarlo desde: https://aria2.github.io/
) else (
    echo [+] aria2c OK.
)

:: 7. Iniciar aria2c en segundo plano (si existe)
if %ARIA2_FOUND%==1 (
    echo.
    echo [+] Iniciando aria2c en segundo plano...
    
    :: Buscar la ruta exacta de aria2c
    for %%p in (
        "%ProgramFiles%\aria2\aria2c.exe"
        "%ProgramFiles(x86)%\aria2\aria2c.exe"
        "%LocalAppData%\Programs\aria2\aria2c.exe"
        "%USERPROFILE%\scoop\apps\aria2\current\aria2c.exe"
    ) do (
        if exist %%p (
            :: Iniciar aria2c como proceso en segundo plano (oculto)
            start /b "" "%%p" --daemon=true --enable-rpc --rpc-listen-port=6800 --rpc-allow-origin-all
            echo [+] aria2c iniciado en puerto 6800
            goto :aria2_started
        )
    )
    :aria2_started
)

:: 8. Lanzar la aplicación en segundo plano
echo.
echo ===================================================
echo    Iniciando Nyaa Desktop Client...
echo ===================================================
echo.

:: Verificar que nyaadesk.py existe
if not exist nyaadesk.py (
    echo [ERROR] No se encuentra nyaadesk.py
    echo Asegurate de que el archivo nyaadesk.py este en esta carpeta.
    pause
    exit
)

start "" pythonw nyaadesk.py

timeout /t 3 >nul

echo.
echo [+] Aplicacion iniciada correctamente.
echo [+] La ventana deberia aparecer en breve.
echo.
echo Presiona cualquier tecla para cerrar este lanzador...
pause >nul
