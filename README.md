<div align="center">

# 🎌 Nyaa Desktop Pro v5.9

**🇪🇸 Español** · [🇬🇧 English](README.en.md)

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00BFFF&center=true&vCenter=true&width=700&lines=Cliente+moderno+para+Nyaa.si;Explora%2C+filtra+y+traduce+tus+torrents;Sube+tus+propios+torrents;Integración+con+AniList;Detección+automática+de+idioma+y+calidad)](https://git.io/typing-svg)

<p align="center">
  <img src="https://img.shields.io/badge/Version-5.9-brightgreen?style=for-the-badge&logo=semantic-release" alt="Version"/>
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
  <a href="#️-aviso-de-responsabilidad">Aviso</a> •
  <a href="#-licencia">Licencia</a> •
  <a href="#-donaciones">Donaciones</a>
</p>

</div>

---

## 📋 Acerca de

**Nyaa Desktop Pro** es un cliente de escritorio moderno para [Nyaa.si](https://nyaa.si), desarrollado íntegramente en Python. Permite explorar la plataforma en tiempo real, filtrar torrents por categoría, ver las descripciones completas traducidas a 14 idiomas, buscar en el catálogo de AniList, descargar mediante enlaces magnet con `aria2` o `transmission-cli`, e incluso iniciar sesión y publicar tus propios torrents sin salir de la app.

---

## 🌟 Características Principales

- **🌐 Feed en vivo y búsqueda universal**  
  Explora el catálogo de Nyaa.si con paginación real.  
  Todas las categorías: Anime, AMV, Audio FLAC/MP3, Manga/Literatura, Live Action, Software y Juegos.  
  Filtros: *Sin filtro*, *No Remakes*, *Solo uploaders confiables*.

- **📖 Detalle de torrents y traductor multilingüe**  
  Abre la descripción completa del uploader con doble clic.  
  Tradúcela a 14 idiomas (Español, Inglés, Francés, Alemán, Ruso, Japonés, Coreano, Chino…) con un clic; siempre se traduce desde el texto original.

- **🎬 Catálogo de AniList**  
  Busca animes por nombre y consulta géneros, puntuación y episodios.  
  Lanza la búsqueda en Nyaa desde cualquier ficha y traduce la sinopsis al español.

- **🔐 Cuenta y subida de torrents**  
  Inicia sesión con cookies persistentes.  
  Sube tus archivos `.torrent` con título, categoría, opciones (Anónimo, Remake, Oculto), enlace de información y descripción en Markdown.

- **🧲 Descargas y detección de idioma/calidad**  
  Detección automática del idioma (Latino, Castellano, Inglés, Raw…) y de la calidad (4K, 1080p, 720p, FLAC).  
  Descarga directa con `aria2` (preferido) o `transmission-cli`; si no hay ninguno, abre el magnet en tu cliente habitual (qBittorrent, Deluge, etc.).

- **⭐ Favoritos**  
  Guarda torrents para abrirlos más tarde, ver sus detalles o lanzar el magnet.

---

### 📸 Vista Previa de la Interfaz

<p align="center">
  <img width="1900" height="1018" alt="Captura de Nyaa Desktop Pro" src="https://github.com/user-attachments/assets/634d0ba3-2abf-4114-8c24-061eb287b07d" />
</p>

## 📋 Requisitos del Sistema

- **Python:** 3.9 o superior, con **tkinter** (en Linux suele ser un paquete aparte: `python3-tk`, `python3-tkinter` o `tk`).
- **Sistema operativo:** Linux, Windows 10/11 o macOS.
- **Cliente BitTorrent (opcional):** `aria2` o `transmission-cli` para descargar desde la app, o cualquier cliente compatible con enlaces magnet.

Las descargas se guardan en `~/Downloads/Anime` (o `~/Descargas/Anime` si tu sistema usa esa carpeta).

---

## 🚀 Instalación y Configuración

### ⚡ Inicio rápido (lanzadores)

- **Windows:** doble clic en `start.bat`. Instala las dependencias de Python que falten y, si no lo encuentra, `aria2` con `winget` (Transmission para Windows no incluye `transmission-cli`, así que en Windows se usa aria2).
- **Linux / macOS:** `bash start.sh`. Instala Python y tkinter si faltan, crea un entorno virtual `env_nyaa` y lanza la app.

### 🐧 Linux

```bash
# 1. Clona el repositorio e ingresa a la carpeta
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Crea y activa un entorno virtual
python3 -m venv venv
source venv/bin/activate          # bash / zsh
# source venv/bin/activate.fish   # fish

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. (Opcional) Instala tkinter y un cliente BitTorrent
# Debian / Ubuntu: sudo apt install python3-tk aria2 transmission-cli
# Arch Linux:      sudo pacman -S tk aria2 transmission-cli
# Fedora:          sudo dnf install python3-tkinter aria2 transmission-cli

# 5. Ejecuta la aplicación
python3 nyaadesk.py
```

### 🪟 Windows

```powershell
# 1. Clona el repositorio
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Crea y activa el entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. (Opcional) Instala un cliente BitTorrent
winget install aria2.aria2

# 5. Ejecuta la aplicación
python nyaadesk.py
```

### 🍎 macOS

```bash
# 1. Clona el proyecto
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Crea y activa el entorno virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. (Opcional) tkinter y cliente BitTorrent vía Homebrew
brew install python-tk aria2 transmission-cli

# 5. Ejecuta la aplicación
python3 nyaadesk.py
```

---

## ⚠️ Aviso de Responsabilidad

Esta aplicación es un cliente de código abierto para interactuar con Nyaa.si y servicios web públicos (AniList / Google Translate). El desarrollador no aloja, distribuye ni controla los contenidos de terceros ni los archivos compartidos a través de redes P2P. El uso de esta herramienta es responsabilidad exclusiva del usuario final.

---

## 📜 Licencia

**MIT License** — consulta el archivo [LICENSE](LICENSE).

---

## 💝 Agradecimientos

- **Nyaa.si** – por el catálogo público.
- **AniList** – por su API GraphQL de anime.
- **CustomTkinter** – por la biblioteca de interfaz gráfica.
- A todos los contribuidores y donantes que hacen posible este proyecto.

## 💖 Donaciones

[Donar con PayPal](https://www.paypal.me/faycraxE)
