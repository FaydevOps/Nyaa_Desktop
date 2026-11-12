<div align="center">

# 🎌 Nyaa Desktop Pro v5.9

[🇪🇸 Español](README.md) · **🇬🇧 English**

[![Typing SVG](https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=00BFFF&center=true&vCenter=true&width=700&lines=Modern+desktop+client+for+Nyaa.si;Browse%2C+filter+and+translate+torrents;Upload+your+own+torrents;AniList+integration;Automatic+language+and+quality+detection)](https://git.io/typing-svg)

<p align="center">
  <img src="https://img.shields.io/badge/Version-5.9-brightgreen?style=for-the-badge&logo=semantic-release" alt="Version"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/Python-3.9+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge&logo=open-source-initiative&logoColor=white" alt="License"/>
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey?style=for-the-badge" alt="Platform"/>
</p>

<p align="center">
  <a href="#-about">About</a> •
  <a href="#-main-features">Features</a> •
  <a href="#-system-requirements">Requirements</a> •
  <a href="#-installation">Installation</a> •
  <a href="#️-disclaimer">Disclaimer</a> •
  <a href="#-license">License</a> •
  <a href="#-donations">Donations</a>
</p>

</div>

> The app's interface is in Spanish.

---

## 📋 About

**Nyaa Desktop Pro** is a modern desktop client for [Nyaa.si](https://nyaa.si), written entirely in Python. Browse the site in real time, filter torrents by category, read full descriptions translated into 14 languages, search the AniList catalog, download through magnet links with `aria2` or `transmission-cli`, and even log in and publish your own torrents without leaving the app.

---

## 🌟 Main Features

- **🌐 Live feed and universal search**  
  Browse the Nyaa.si catalog with real pagination.  
  Every category: Anime, AMV, FLAC/MP3 audio, Manga/Literature, Live Action, Software and Games.  
  Filters: *No filter*, *No remakes*, *Trusted uploaders only*.

- **📖 Torrent details and multilingual translator**  
  Double-click a torrent to open the uploader's full description.  
  Translate it into 14 languages (Spanish, English, French, German, Russian, Japanese, Korean, Chinese…) with one click; translation always starts from the original text.

- **🎬 AniList catalog**  
  Search anime by name and see genres, score and episode count.  
  Jump to a Nyaa search from any entry and translate the synopsis into Spanish.

- **🔐 Account and torrent upload**  
  Log in with persistent cookies.  
  Upload your `.torrent` files with title, category, flags (Anonymous, Remake, Hidden), information link and Markdown description.

- **🧲 Downloads and language/quality detection**  
  Automatic detection of language (Latin American Spanish, Castilian Spanish, English, Raw…) and quality (4K, 1080p, 720p, FLAC).  
  Direct download with `aria2` (preferred) or `transmission-cli`; if neither is installed, the magnet opens in your usual client (qBittorrent, Deluge, etc.).

- **⭐ Favorites**  
  Save torrents to open later, view their details or launch the magnet.

---

### 📸 Interface Preview

<p align="center">
  <img width="1900" height="1018" alt="Nyaa Desktop Pro screenshot" src="https://github.com/user-attachments/assets/634d0ba3-2abf-4114-8c24-061eb287b07d" />
</p>

## 📋 System Requirements

- **Python:** 3.9 or newer, with **tkinter** (on Linux it is usually a separate package: `python3-tk`, `python3-tkinter` or `tk`).
- **Operating system:** Linux, Windows 10/11 or macOS.
- **BitTorrent client (optional):** `aria2` or `transmission-cli` to download from the app, or any client that handles magnet links.

Downloads are saved to `~/Downloads/Anime` (or `~/Descargas/Anime` if your system uses that folder).

---

## 🚀 Installation

### ⚡ Quick start (launchers)

- **Windows:** double-click `start.bat`. It installs any missing Python dependencies and, if not found, `aria2` through `winget` (Transmission for Windows does not ship `transmission-cli`, so aria2 is used on Windows).
- **Linux / macOS:** `bash start.sh`. It installs Python and tkinter if missing, creates an `env_nyaa` virtual environment and launches the app.

### 🐧 Linux

```bash
# 1. Clone the repository and enter the folder
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # bash / zsh
# source venv/bin/activate.fish   # fish

# 3. Install the dependencies
pip install -r requirements.txt

# 4. (Optional) Install tkinter and a BitTorrent client
# Debian / Ubuntu: sudo apt install python3-tk aria2 transmission-cli
# Arch Linux:      sudo pacman -S tk aria2 transmission-cli
# Fedora:          sudo dnf install python3-tkinter aria2 transmission-cli

# 5. Run the app
python3 nyaadesk.py
```

### 🪟 Windows

```powershell
# 1. Clone the repository
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Create and activate the virtual environment
python -m venv venv
.\venv\Scripts\activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. (Optional) Install a BitTorrent client
winget install aria2.aria2

# 5. Run the app
python nyaadesk.py
```

### 🍎 macOS

```bash
# 1. Clone the project
git clone https://github.com/FaydevOps/Nyaa_Desktop
cd Nyaa_Desktop

# 2. Create and activate the virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install the dependencies
pip install -r requirements.txt

# 4. (Optional) tkinter and a BitTorrent client via Homebrew
brew install python-tk aria2 transmission-cli

# 5. Run the app
python3 nyaadesk.py
```

---

## ⚠️ Disclaimer

This application is an open-source client for interacting with Nyaa.si and public web services (AniList / Google Translate). The developer does not host, distribute or control third-party content or files shared over P2P networks. Use of this tool is the sole responsibility of the end user.

---

## 📜 License

**MIT License** — see the [LICENSE](LICENSE) file.

---

## 💝 Acknowledgements

- **Nyaa.si** – for the public catalog.
- **AniList** – for its anime GraphQL API.
- **CustomTkinter** – for the GUI library.
- All the contributors and donors who make this project possible.

## 💖 Donations

[Donate with PayPal](https://www.paypal.me/faycraxE)
