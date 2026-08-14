<div align="center">

# 🎌 Nyaa Desktop Pro v5.1


[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00BFFF&center=true&vCenter=true&width=700&lines=Cliente+moderno+para+Nyaa.si;Explora%2C+filtra+y+traduce+tus+torrents;Sube+tus+propios+torrents;Integración+con+AniList+%26+MyAnimeList;Detección+automática+de+idioma+y+calidad)](https://git.io/typing-svg)

<p align="center">
  <img src="https://img.shields.io/badge/Version-5.1-brightgreen?style=for-the-badge&logo=semantic-release" alt="Version"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License"/>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge" alt="Platform"/>
</p>

<p align="center">
  <a href="#-acerca-de">Acerca de</a> •
  <a href="#-características-principales">Características</a> •
  <a href="#-requisitos-del-sistema">Requisitos</a> •
  <a href="#-instalación-y-configuración">Instalación</a> •
  <a href="#-archivo-requirementstxt">requirements.txt</a> •
  <a href="#-uso">Uso</a> •
  <a href="#-capturas-de-pantalla">Capturas</a> •
  <a href="#-apoya-el-proyecto-donaciones">Donaciones</a> •
  <a href="#-licencia">Licencia</a> •
  <a href="#-aviso-de-responsabilidad">Aviso</a> •
  <a href="#-créditos">Créditos</a>
</p>

</div>

---

## 📋 Acerca de

**Nyaa Desktop Pro** es un cliente de escritorio completo, moderno y de alto rendimiento para [Nyaa.si](https://nyaa.si), desarrollado íntegramente en Python. Permite explorar la plataforma en tiempo real, filtrar torrents por idioma y categorías, ver descripciones completas traducidas automáticamente a más de 15 idiomas, integrar el catálogo con AniList, gestionar descargas mediante enlaces Magnet / `transmission-cli` `Aira2` e incluso iniciar sesión y publicar tus propios torrents sin salir de la app.

---

## 🌟 Características Principales

- **🌐 Feed en Vivo y Búsqueda Universal**  
  Explora el catálogo en vivo de Nyaa.si con paginación real (Pág 1, 2, 3...).  
  Soporte completo para todas las categorías: Anime, AMV, Audio FLAC/MP3, Manga/Literatura, Live Action, Software, Juegos.  
  Filtros de confianza: *Todos los torrents*, *Solo Uploaders Confiables*, *No Remakes*.

- **📖 Detalle de Torrents y Traductor Multilingüe**  
  Abre las descripciones completas publicadas por los uploaders con doble clic.  
  Traducción automática instantánea: traduce la descripción del torrent o las sinopsis de anime a más de 15 idiomas (Español, Inglés, Francés, Alemán, Ruso, Japonés, etc.) con un solo clic.

- **🎬 Catálogo Integrado con AniList & MyAnimeList**  
  Busca animes directamente por nombre, visualiza carátulas, géneros, puntuaciones y episodios.  
  Lanza búsquedas instantáneas en Nyaa desde cualquier ficha del catálogo.

- **🔐 Gestión de Cuenta y Subida de Torrents (/upload)**  
  Inicia sesión de forma segura manteniendo cookies persistentes en tu sistema.  
  Uploader integrado: sube tus propios archivos `.torrent` asignando títulos, categorías, etiquetas (Anónimo, Remake, Oculto), enlaces de información y descripciones formatadas en Markdown.

- **🧲 Integración BitTorrent & Detección de Idioma**  
  Detección automática del idioma del torrent (Español Latino, Castellano, Inglés, Raw, etc.) e indicadores visuales de calidad (4K, 1080p, 720p, FLAC).  
  Integración nativa con `transmission-cli` para descargas directas o apertura automática de enlaces magnet en tu cliente de escritorio habitual (qBittorrent, Transmission GTK, Deluge, etc.).

- **⭐ Favoritos y Personalización**  
  Guarda torrents en marcadores locales para descargarlos o seguirlos más tarde.  
  Interfaz moderna en Modo Oscuro (Cyber‑Glass UI) adaptable y fluida.

---

### 📸 Vista Previa de la Interfaz (GUI)

<p align="center">
  <img width="1900" height="1018" alt="image" src="https://github.com/user-attachments/assets/634d0ba3-2abf-4114-8c24-061eb287b07d" />
</p>

## 📋 Requisitos del Sistema

- **Python:** 3.9 o superior.
- **Sistema Operativo:** Linux, Windows 10/11 o macOS.
- **Cliente BitTorrent (Opcional):** `transmission-cli` (para descargas CLI automatizadas) o cualquier cliente Torrent compatible con enlaces magnet (qBittorrent, Deluge, etc.).

---

## 🚀 Instalación y Configuración

Sigue estos pasos según tu sistema operativo para clonar el repositorio y ejecutar la aplicación.


### 🐧 Linux / macOS / Arch / Deb

```bash

# 1. Clona el repositorio e ingresa a la carpeta
git clone [https://github.com/tu-usuario/nyaa-desktop-pro.git](https://github.com/tu-usuario/nyaa-desktop-pro.git)
cd nyaa-desktop-pro

# 2. Crea y activa un entorno virtual (Recomendado en Python 3.12+)
python3 -m venv venv
#arch#
source venv/bin/activate.fish
#macos deb#
source venv/bin/activate

# 3. Instala las dependencias necesarias
pip install requests beautifulsoup4 pillow customtkinter

# 4. (Opcional) Instala transmission-cli para descargas automáticas
# Ubuntu / Debian: sudo apt install transmission-cli
# Arch Linux:      sudo pacman -S transmission-cli
# Fedora:          sudo dnf install transmission-cli

# 5. Ejecuta la aplicación
python3 nyadowloader.py


```

### 🪟 Windows

```cmd
# 1. Abre PowerShell o CMD y clona el repositorio
git clone [https://github.com/tu-usuario/nyaa-desktop-pro.git](https://github.com/tu-usuario/nyaa-desktop-pro.git)
cd nyaa-desktop-pro

# 2. Crea y activa el entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instala las dependencias
pip install requests beautifulsoup4 pillow customtkinter

# 4. Ejecuta la aplicación
python nyadowloader.py
```

### 🍎 macOS

```bash
# 1. Abre la Terminal y clona el proyecto
git clone [https://github.com/tu-usuario/nyaa-desktop-pro.git](https://github.com/tu-usuario/nyaa-desktop-pro.git)
cd nyaa-desktop-pro

# 2. Crea y activa el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instala las dependencias requeridas
pip install requests beautifulsoup4 pillow customtkinter

# 4. (Opcional) Instala transmission-cli vía Homebrew
brew install transmission-cli

# 5. Ejecuta la aplicación
python3 nyadowloader.py

```


## ⚠️ Disclaimer

Esta aplicación es una interfaz de cliente de código abierto para interactuar con Nyaa.si y servicios web públicos (AniList / Google Translate). El desarrollador no aloja, distribuye ni controla los contenidos de terceros ni los archivos compartidos a través de redes P2P. El uso de esta herramienta es responsabilidad exclusiva del usuario final.

---

### 📜 License

**MIT License**

---

### 💝 Agradecimientos
Nyaa.si – Por proporcionar el catálogo público.

AniList – Por su API GraphQL para consulta de anime.

CustomTkinter – Por la moderna biblioteca de interfaz gráfica.

A todos los contribuidores y donantes que hacen posible este proyecto.

</div>

### Donaciones 
[Donate](https://www.paypal.me/faycraxE)

---

<div align="center">
