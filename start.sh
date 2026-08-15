#!/bin/bash
# start_nyaa.sh – Lanzador para Nyaa Desktop Client
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
            sudo pacman -Syu --noconfirm "${packages[@]}"
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
    echo -e "${YELLOW}🚀 Iniciando instalación de Nyaa Desktop Client...${NC}"

    detect_os
    detect_package_manager

    local deps=()
    if [[ "$OS" == "macos" ]]; then
        deps=("python3")  # Homebrew instalará pip y venv junto con python3
    else
        deps=("python3" "python3-pip" "python3-venv")
        if [[ "$PKG_MANAGER" == "pacman" ]]; then
            deps=("python" "python-pip")   # Arch
        fi
        if [[ "$PKG_MANAGER" == "apk" ]]; then
            deps=("python3" "py3-pip" "py3-virtualenv")
        fi
        if [[ "$PKG_MANAGER" == "yum" ]]; then
            deps=("python3" "python3-pip" "python3-virtualenv")
        fi
    fi

    echo -e "${YELLOW}📥 Instalando dependencias del sistema: ${deps[*]}${NC}"
    install_packages "${deps[@]}"

    if [ ! -d "env_nyaa" ]; then
        echo -e "${YELLOW}🔧 Creando entorno virtual...${NC}"
        python3 -m venv env_nyaa
    else
        echo -e "${GREEN}✅ Entorno virtual ya existe.${NC}"
    fi

    source env_nyaa/bin/activate

    echo -e "${YELLOW}📦 Actualizando pip...${NC}"
    python3 -m pip install --upgrade pip

    echo -e "${YELLOW}📦 Instalando dependencias Python...${NC}"
    pip install requests beautifulsoup4 pillow customtkinter

    if [ -f "requirements.txt" ]; then
        echo -e "${YELLOW}📦 Instalando desde requirements.txt...${NC}"
        pip install -r requirements.txt
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
