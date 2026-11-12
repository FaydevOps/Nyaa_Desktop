@echo off
title Nyaa Desktop Client - Lanzador
cd /d "%~dp0"

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
    exit /b 1
)

:: 2. Instalar dependencias de Python solo si faltan
python -c "import customtkinter, requests, bs4, PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo [+] Instalando dependencias desde requirements.txt...
    python -m pip install --user -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] No se pudieron instalar las dependencias.
        pause
        exit /b 1
    )
)

:: 3. Buscar aria2 (PATH y rutas tipicas); instalar con winget solo si no existe.
::    Transmission no se instala: su paquete de Windows solo trae la GUI, sin transmission-cli.
call :buscar aria2c.exe ARIA2_PATH "%LocalAppData%\Microsoft\WinGet\Links\aria2c.exe" "%ProgramFiles%\aria2\aria2c.exe" "%LocalAppData%\Programs\aria2\aria2c.exe" "%USERPROFILE%\scoop\shims\aria2c.exe"
if not defined ARIA2_PATH (
    echo [+] Instalando aria2 con winget...
    winget install --id aria2.aria2 -e --silent --accept-package-agreements --accept-source-agreements
)

:: 4. Verificar que nyaadesk.py existe
if not exist nyaadesk.py (
    echo [ERROR] No se encuentra nyaadesk.py
    pause
    exit /b 1
)

:: 5. Lanzar la aplicacion sin consola (pythonw) y cerrar el lanzador
echo.
echo Iniciando Nyaa Desktop Client...
where pythonw >nul 2>nul
if %errorlevel% equ 0 (
    start "" pythonw nyaadesk.py
) else (
    start "" python nyaadesk.py
)
exit /b 0

:: --- :buscar <exe> <variable> <rutas...> : PATH primero, luego las rutas dadas ---
:buscar
set "_var=%~2"
set "%_var%="
for /f "delims=" %%r in ('where %~1 2^>nul') do if not defined %_var% set "%_var%=%%r"
shift
shift
:buscar_loop
if "%~1"=="" exit /b 0
if not defined %_var% if exist "%~1" set "%_var%=%~1"
shift
goto buscar_loop
