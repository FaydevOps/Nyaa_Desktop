#!/bin/bash
# start.sh – Lanzador para Nyaa Desktop Client
# Compatible con: Debian/Ubuntu, Arch, Fedora, RHEL/CentOS, openSUSE, Alpine, macOS (Homebrew)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$ID
        else
            OS="linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        OS="unknown"
    fi
    echo -e "${GREEN}🔍 Sistema detectado: $OS${NC}"
}

detect_package_manager() {
    if command -v apt &>/dev/null; then
        PKG_MANAGER="apt"
    elif command -v pacman &>/dev/null; then
        PKG_MANAGER="pacman"
    elif command -v dnf &>/dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &>/dev/null; then
        PKG_MANAGER="yum"
    elif command -v zypper &>/dev/null; then
        PKG_MANAGER="zypper"
    elif command -v apk &>/dev/null; then
        PKG_MANAGER="apk"
    elif command -v brew &>/dev/null; then
        PKG_MANAGER="brew"
    else
        PKG_MANAGER="unknown"
    fi
    echo -e "${GREEN}📦 Gestor de paquetes: $PKG_MANAGER${NC}"
}

install_packages() {
    local packages=("$@")
    case $PKG_MANAGER in
        apt)
            sudo apt update && sudo apt install -y "${packages[@]}"
            ;;
        pacman)
            sudo pacman -S --needed --noconfirm "${packages[@]}"
            ;;
        dnf)
            sudo dnf install -y "${packages[@]}"
            ;;
        yum)
            sudo yum install -y "${packages[@]}"
            ;;
        zypper)
            sudo zypper install -y "${packages[@]}"
            ;;
        apk)
            sudo apk add "${packages[@]}"
            ;;
        brew)
            brew install "${packages[@]}"
            ;;
        *)
            echo -e "${RED}❌ Gestor no soportado. Instala manualmente: ${packages[*]}${NC}"
            exit 1
            ;;
    esac
}

main() {
    cd "$(dirname "$0")"
    echo -e "${YELLOW}🚀 Iniciando instalación de Nyaa Desktop Client...${NC}"

    detect_os
    detect_package_manager

    local deps=()
    if [[ "$OS" == "macos" ]]; then
        deps=("python3" "python-tk")  # Homebrew instala pip y venv junto con python3
    else
        # tkinter es obligatorio para customtkinter y no viene con python3 en la mayoría de distros
        case $PKG_MANAGER in
            pacman) deps=("python" "python-pip" "tk") ;;
            apk)    deps=("python3" "py3-pip" "py3-virtualenv" "py3-tkinter") ;;
            dnf|yum) deps=("python3" "python3-pip" "python3-tkinter") ;;
            zypper) deps=("python3" "python3-pip" "python3-tk") ;;
            *)      deps=("python3" "python3-pip" "python3-venv" "python3-tk") ;;
        esac
    fi

    # Solo pedir sudo/instalar si falta Python, venv o tkinter
    if command -v python3 &>/dev/null && python3 -c "import tkinter, venv" &>/dev/null; then
        echo -e "${GREEN}✅ Python 3 con tkinter ya instalado.${NC}"
    else
        echo -e "${YELLOW}📥 Instalando dependencias del sistema: ${deps[*]}${NC}"
        install_packages "${deps[@]}"
    fi

    if [ ! -d "env_nyaa" ]; then
        echo -e "${YELLOW}🔧 Creando entorno virtual...${NC}"
        python3 -m venv env_nyaa
    else
        echo -e "${GREEN}✅ Entorno virtual ya existe.${NC}"
    fi

    source env_nyaa/bin/activate

    if ! python3 -c "import customtkinter, requests, bs4, PIL" &>/dev/null; then
        echo -e "${YELLOW}📦 Instalando dependencias Python desde requirements.txt...${NC}"
        python3 -m pip install --upgrade pip
        python3 -m pip install -r requirements.txt
    else
        echo -e "${GREEN}✅ Dependencias Python ya instaladas.${NC}"
    fi

    if [ -f "nyaadesk.py" ]; then
        echo -e "${GREEN}🚀 Lanzando Nyaa Desktop...${NC}"
        python3 nyaadesk.py > /dev/null 2>&1 &
        sleep 2
        echo -e "${GREEN}✅ Aplicación iniciada. Puedes cerrar esta terminal.${NC}"
    else
        echo -e "${RED}❌ No se encontró nyaadesk.py. Verifica el directorio.${NC}"
        exit 1
    fi

    deactivate
}

main
