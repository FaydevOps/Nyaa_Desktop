#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🎌 Nyaa Desktop Client & Anime Downloader Pro v5.1
==================================================
Una aplicación completa de escritorio para explorar, buscar, ver detalles,
descargar y subir torrents a Nyaa.si con integraciones con AniList,
gestión de sesiones y soporte para clientes BitTorrent.
"""

import sys
import os
import platform
import threading
import time
import urllib.parse
import hashlib
import io
import json
import subprocess
import re
from datetime import datetime

# Librerías de terceros (deben estar instaladas previamente)
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

SISTEMA = platform.system()
ES_WINDOWS = SISTEMA == "Windows"
ES_MAC = SISTEMA == "Darwin"
ES_LINUX = SISTEMA == "Linux"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def obtener_carpeta_descargas():
    if ES_WINDOWS:
        return os.path.join(os.environ.get('USERPROFILE', ''), 'Descargas', 'Anime')
    elif ES_MAC:
        return os.path.join(os.path.expanduser('~'), 'Downloads', 'Anime')
    else:
        return os.path.join(os.path.expanduser('~'), 'Descargas', 'Anime')

def obtener_carpeta_config():
    if ES_WINDOWS:
        return os.path.join(os.environ.get('APPDATA', ''), 'NyaaDesktopPro')
    elif ES_MAC:
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', 'NyaaDesktopPro')
    else:
        return os.path.join(os.path.expanduser('~'), '.config', 'nyaa_desktop_pro')

def abrir_recurso(target):
    """Abre una URL o archivo local con el programa predeterminado del sistema."""
    try:
        if ES_WINDOWS:
            os.startfile(target)
        elif ES_MAC:
            subprocess.Popen(['open', target])
        else:
            subprocess.Popen(['xdg-open', target])
        return True
    except Exception as e:
        print(f"Error abriendo recurso: {e}")
        return False

def copiar_al_portapapeles(texto, window):
    """Copia una cadena de texto al portapapeles."""
    window.clipboard_clear()
    window.clipboard_append(texto)
    window.update()

def detectar_transmission():
    """
    Detecta si transmission-cli está disponible en el sistema.
    En Windows busca en rutas comunes y usa 'where'.
    """
    if ES_WINDOWS:
        # Primero intentar con 'where'
        try:
            result = subprocess.run(['where', 'transmission-cli'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        # Buscar en rutas comunes de instalación
        common_paths = [
            r"C:\Program Files\Transmission\bin\transmission-cli.exe",
            r"C:\Program Files (x86)\Transmission\bin\transmission-cli.exe",
            r"C:\ProgramData\chocolatey\bin\transmission-cli.exe",
            os.path.expanduser(r"~\scoop\shims\transmission-cli.exe")
        ]
        for path in common_paths:
            if os.path.exists(path):
                return True
        return False
    else:
        # Linux/Mac: usar 'which'
        try:
            result = subprocess.run(['which', 'transmission-cli'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

def detectar_aria2():
    """
    Detecta si aria2c está disponible en el sistema.
    En Windows busca en rutas comunes y usa 'where'.
    """
    if ES_WINDOWS:
        # Primero intentar con 'where'
        try:
            result = subprocess.run(['where', 'aria2c'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        # Buscar en rutas comunes de instalación
        common_paths = [
            r"C:\Program Files\aria2\aria2c.exe",
            r"C:\Program Files (x86)\aria2\aria2c.exe",
            r"C:\ProgramData\chocolatey\bin\aria2c.exe",
            os.path.expanduser(r"~\scoop\shims\aria2c.exe")
        ]
        for path in common_paths:
            if os.path.exists(path):
                return True
        return False
    else:
        # Linux/Mac: usar 'which'
        try:
            result = subprocess.run(['which', 'aria2c'], capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False

def detectar_idioma_torrent(nombre):
    """Detecta el idioma de un título de torrent retornando (idioma, emoji, color_hex)."""
    if not nombre:
        return ('Desconocido', '🌐', '#6B7280')
    
    nombre_lower = nombre.lower()
    
    dict_idiomas = {
        'Español Latino': {
            'keywords': ['latino', 'lat', 'doblaje latino', 'esp lat', 'es-lat', 'spanish latino'],
            'emoji': '🌎',
            'color': '#EF4444'
        },
        'Español Castellano': {
            'keywords': ['español', 'castellano', 'sub español', 'audio español', 'esp', 'es-', 'spanish'],
            'emoji': '🇪🇸',
            'color': '#F59E0B'
        },
        'Inglés': {
            'keywords': ['english', 'sub english', 'audio english', 'eng', 'en-', 'dual audio'],
            'emoji': '🇬🇧',
            'color': '#3B82F6'
        },
        'Japonés Raw': {
            'keywords': ['japanese', 'jap', 'ja-', 'raw'],
            'emoji': '🇯🇵',
            'color': '#EC4899'
        },
        'Francés': {
            'keywords': ['french', 'francais', 'vostfr', 'fr-'],
            'emoji': '🇫🇷',
            'color': '#10B981'
        },
        'Alemán': {
            'keywords': ['german', 'deutsch', 'ger', 'de-'],
            'emoji': '🇩🇪',
            'color': '#8B5CF6'
        },
        'Italiano': {
            'keywords': ['italian', 'italiano', 'ita', 'it-'],
            'emoji': '🇮🇹',
            'color': '#14B8A6'
        },
        'Portugués': {
            'keywords': ['portuguese', 'português', 'pt-br', 'pt-'],
            'emoji': '🇧🇷',
            'color': '#F97316'
        },
        'Ruso': {
            'keywords': ['russian', 'ruso', 'ru-'],
            'emoji': '🇷🇺',
            'color': '#6366F1'
        }
    }
    
    for idioma, info in dict_idiomas.items():
        for kw in info['keywords']:
            if kw in nombre_lower:
                return (idioma, info['emoji'], info['color'])
                
    return ('General / Multi', '🌐', '#6B7280')

def detectar_calidad(nombre):
    nombre_l = nombre.lower()
    if '2160p' in nombre_l or '4k' in nombre_l:
        return '4K UHD'
    elif '1080p' in nombre_l or 'fhd' in nombre_l:
        return '1080p'
    elif '720p' in nombre_l or 'hd' in nombre_l:
        return '720p'
    elif '480p' in nombre_l or 'sd' in nombre_l:
        return '480p'
    elif 'flac' in nombre_l or 'lossless' in nombre_l:
        return 'Audio Hi-Res'
    return 'Estándar'

# ============================================
# TRADUCTOR MULTILINGÜE DE DESCRIPCIONES
# ============================================
IDIOMAS_TRADUCCION = {
    "Español": "es",
    "Inglés": "en",
    "Francés": "fr",
    "Alemán": "de",
    "Italiano": "it",
    "Português": "pt",
    "Ruso": "ru",
    "Japonés": "ja",
    "Coreano": "ko",
    "Chino (Simplificado)": "zh-CN",
    "Árabe": "ar",
    "Turco": "tr",
    "Polaco": "pl",
    "Holandés": "nl"
}

def traducir_texto(texto, target_lang='es'):
    """Traduce cualquier texto o descripción al idioma deseado usando endpoint gratuito."""
    if not texto or not texto.strip():
        return texto
    try:
        lineas = texto.split('\n')
        resultado = []
        bloque = ""
        for linea in lineas:
            if len(bloque) + len(linea) < 1000:
                bloque += linea + "\n"
            else:
                resultado.append(_traducir_chunk(bloque, target_lang))
                bloque = linea + "\n"
        if bloque:
            resultado.append(_traducir_chunk(bloque, target_lang))
            
        return "".join(resultado)
    except Exception as e:
        print(f"Error traduciendo texto: {e}")
        return texto

def _traducir_chunk(chunk, target_lang):
    if not chunk.strip():
        return chunk
    try:
        params = {
            'client': 'gtx',
            'sl': 'auto',
            'tl': target_lang,
            'dt': 't',
            'q': chunk
        }
        url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode(params)
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                partes = [item[0] for item in data[0] if item and len(item) > 0 and item[0]]
                return "".join(partes)
    except Exception as e:
        print(f"Error en chunk de traducción: {e}")
    return chunk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NyaaDesktopApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🎌 Nyaa Desktop Pro - Cliente & Búsqueda Universal")
        self.window.geometry("1400x880")
        self.window.minsize(1100, 700)
        
        # Rutas del sistema y configuración
        self.dir_descargas = obtener_carpeta_descargas()
        self.dir_config = obtener_carpeta_config()
        self.dir_cache = os.path.join(self.dir_config, 'cache_img')
        self.file_favs = os.path.join(self.dir_config, 'favoritos.json')
        self.file_cookies = os.path.join(self.dir_config, 'session_cookies.json')
        
        for d in [self.dir_descargas, self.dir_config, self.dir_cache]:
            os.makedirs(d, exist_ok=True)
            
        # Variables de estado
        self.session = requests.Session()
        self.session.headers.update(HEADERS)
        self.usuario_logueado = None
        self.cargar_cookies_sesion()
        
        self.favoritos = self.cargar_favoritos()
        self.torrents_lista = []
        self.torrents_filtrados = []
        self.animes_catalogo = []
        self.descargas_activas = []
        self.transmission_disponible = detectar_transmission()
        self.aria2_disponible = detectar_aria2()
        
        self.crear_interfaz()
        self.comprobar_estado_usuario()
        
        # Cargar feed principal de Nyaa al iniciar
        self.window.after(300, self.cargar_feed_nyaa)
        
        self.window.mainloop()

    def cargar_cookies_sesion(self):
        """Carga las cookies guardadas previamente para mantener la sesión abierta."""
        if os.path.exists(self.file_cookies):
            try:
                with open(self.file_cookies, 'r', encoding='utf-8') as f:
                    cookies_dict = json.load(f)
                    self.session.cookies.update(cookies_dict)
            except Exception as e:
                print(f"Error al cargar cookies: {e}")

    def guardar_cookies_sesion(self):
        """Guarda las cookies de la sesión activa en disco."""
        try:
            with open(self.file_cookies, 'w', encoding='utf-8') as f:
                json.dump(self.session.cookies.get_dict(), f, indent=2)
        except Exception as e:
            print(f"Error guardando cookies: {e}")

    def comprobar_estado_usuario(self):
        """Verifica si la sesión guardada sigue siendo válida en Nyaa.si."""
        def _check():
            try:
                res = self.session.get("https://nyaa.si/", timeout=10)
                soup = BeautifulSoup(res.text, 'html.parser')
                nav_user = soup.find('a', href=re.compile(r'/user/'))
                if nav_user:
                    self.usuario_logueado = nav_user.text.strip()
                    self.window.after(0, lambda: self.lbl_user_status.configure(
                        text=f"👤 Conectado: {self.usuario_logueado}", text_color="#10B981"
                    ))
                    self.window.after(0, lambda: self.btn_login_sidebar.configure(text="🚪 Cerrar Sesión"))
                else:
                    self.usuario_logueado = None
                    self.window.after(0, lambda: self.lbl_user_status.configure(
                        text="👤 Modo Invitado", text_color="#9CA3AF"
                    ))
                    self.window.after(0, lambda: self.btn_login_sidebar.configure(text="🔑 Iniciar Sesión"))
            except Exception as e:
                print(f"No se pudo verificar sesión: {e}")
        
        threading.Thread(target=_check, daemon=True).start()

    def crear_interfaz(self):
        # Contenedor raíz dividido en Sidebar + Contenido Principal
        self.root_frame = ctk.CTkFrame(self.window, fg_color="#0F1117")
        self.root_frame.pack(fill="both", expand=True)

        # BARRA LATERAL (Sidebar)
        self.sidebar = ctk.CTkFrame(self.root_frame, width=220, corner_radius=0, fg_color="#161922")
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        # Logo / Título app
        lbl_logo = ctk.CTkLabel(
            self.sidebar, text="🎌 NYAA PRO", font=("Segoe UI", 22, "bold"), text_color="#3B82F6"
        )
        lbl_logo.pack(padx=20, pady=(20, 5), anchor="w")

        lbl_sub = ctk.CTkLabel(
            self.sidebar, text="Desktop Client v5.1", font=("Segoe UI", 11), text_color="#6B7280"
        )
        lbl_sub.pack(padx=20, pady=(0, 20), anchor="w")

        # Indicador Usuario
        self.lbl_user_status = ctk.CTkLabel(
            self.sidebar, text="👤 Comprobando...", font=("Segoe UI", 12, "bold"), text_color="#9CA3AF"
        )
        self.lbl_user_status.pack(padx=20, pady=(0, 10), anchor="w")

        # Botón Login / Logout
        self.btn_login_sidebar = ctk.CTkButton(
            self.sidebar, text="🔑 Iniciar Sesión", font=("Segoe UI", 12),
            fg_color="#1F2937", hover_color="#374151", height=32, command=self.abrir_dialogo_login
        )
        self.btn_login_sidebar.pack(padx=15, pady=(0, 25), fill="x")

        # Divisor
        ctk.CTkFrame(self.sidebar, height=1, fg_color="#2D3748").pack(fill="x", padx=15, pady=10)

        # Botones Navegación
        self.btn_nav_feed = ctk.CTkButton(
            self.sidebar, text="🌐 Nyaa Live Feed", font=("Segoe UI", 13, "bold"),
            fg_color="#2563EB", hover_color="#1D4ED8", anchor="w", height=38, command=self.mostrar_tab_feed
        )
        self.btn_nav_feed.pack(padx=15, pady=5, fill="x")

        self.btn_nav_anilist = ctk.CTkButton(
            self.sidebar, text="🎬 Catálogo AniList", font=("Segoe UI", 13),
            fg_color="transparent", hover_color="#1F2937", anchor="w", height=38, command=self.mostrar_tab_anilist
        )
        self.btn_nav_anilist.pack(padx=15, pady=5, fill="x")

        self.btn_nav_upload = ctk.CTkButton(
            self.sidebar, text="📤 Subir Torrent", font=("Segoe UI", 13),
            fg_color="transparent", hover_color="#1F2937", anchor="w", height=38, command=self.mostrar_tab_upload
        )
        self.btn_nav_upload.pack(padx=15, pady=5, fill="x")

        self.btn_nav_favs = ctk.CTkButton(
            self.sidebar, text="⭐ Mis Favoritos", font=("Segoe UI", 13),
            fg_color="transparent", hover_color="#1F2937", anchor="w", height=38, command=self.mostrar_tab_favs
        )
        self.btn_nav_favs.pack(padx=15, pady=5, fill="x")

        self.btn_nav_downloads = ctk.CTkButton(
            self.sidebar, text="📥 Descargas", font=("Segoe UI", 13),
            fg_color="transparent", hover_color="#1F2937", anchor="w", height=38, command=self.mostrar_tab_downloads
        )
        self.btn_nav_downloads.pack(padx=15, pady=5, fill="x")

        # Footer Sidebar con estado de clientes BitTorrent
        frame_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        frame_footer.pack(side="bottom", fill="x", padx=15, pady=15)

        tb_status = "✅ Transmission OK" if self.transmission_disponible else "⚠️ Transmission no encontrado"
        tb_color = "#10B981" if self.transmission_disponible else "#F59E0B"
        ctk.CTkLabel(frame_footer, text=tb_status, font=("Segoe UI", 11), text_color=tb_color).pack(anchor="w")

        aria_status = "✅ aria2 OK" if self.aria2_disponible else "⚠️ aria2 no encontrado"
        aria_color = "#10B981" if self.aria2_disponible else "#F59E0B"
        ctk.CTkLabel(frame_footer, text=aria_status, font=("Segoe UI", 11), text_color=aria_color).pack(anchor="w")

        # CONTENEDOR PRINCIPAL
        self.main_content = ctk.CTkFrame(self.root_frame, fg_color="#0F1117")
        self.main_content.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # Tab Views
        self.tabview = ctk.CTkTabview(self.main_content, fg_color="#12141D")
        self.tabview.pack(fill="both", expand=True)

        self.tab_feed = self.tabview.add("Feed Nyaa")
        self.tab_anilist = self.tabview.add("AniList")
        self.tab_upload = self.tabview.add("Subir Torrent")
        self.tab_favs = self.tabview.add("Favoritos")
        self.tab_downloads = self.tabview.add("Gestor Descargas")

        # Ocultar pestañas superiores de CustomTkinter para navegación limpia por sidebar
        self.tabview._segmented_button.grid_forget()

        self.crear_tab_feed()
        self.crear_tab_anilist()
        self.crear_tab_upload()
        self.crear_tab_favs()
        self.crear_tab_downloads()

        # Status Bar Inferior
        self.status_bar = ctk.CTkFrame(self.main_content, height=28, fg_color="#161922")
        self.status_bar.pack(fill="x", pady=(10, 0))

        self.lbl_status = ctk.CTkLabel(
            self.status_bar, text="Listo. Explora o busca contenidos.", font=("Segoe UI", 12), text_color="#9CA3AF"
        )
        self.lbl_status.pack(side="left", padx=10)

    def reset_nav_buttons(self):
        for btn in [self.btn_nav_feed, self.btn_nav_anilist, self.btn_nav_upload, self.btn_nav_favs, self.btn_nav_downloads]:
            btn.configure(fg_color="transparent")

    def mostrar_tab_feed(self):
        self.reset_nav_buttons()
        self.btn_nav_feed.configure(fg_color="#2563EB")
        self.tabview.set("Feed Nyaa")

    def mostrar_tab_anilist(self):
        self.reset_nav_buttons()
        self.btn_nav_anilist.configure(fg_color="#2563EB")
        self.tabview.set("AniList")

    def mostrar_tab_upload(self):
        if not self.usuario_logueado:
            messagebox.showwarning("Sesión requerida", "Debes iniciar sesión con tu cuenta de Nyaa.si para subir torrents.")
            self.abrir_dialogo_login()
            return
        self.reset_nav_buttons()
        self.btn_nav_upload.configure(fg_color="#2563EB")
        self.tabview.set("Subir Torrent")

    def mostrar_tab_favs(self):
        self.reset_nav_buttons()
        self.btn_nav_favs.configure(fg_color="#2563EB")
        self.tabview.set("Favoritos")
        self.actualizar_vista_favoritos()

    def mostrar_tab_downloads(self):
        self.reset_nav_buttons()
        self.btn_nav_downloads.configure(fg_color="#2563EB")
        self.tabview.set("Gestor Descargas")

    def crear_tab_feed(self):
        # Controles superiores
        top_frame = ctk.CTkFrame(self.tab_feed, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        # Entrada búsqueda
        self.entry_nyaa_search = ctk.CTkEntry(
            top_frame, placeholder_text="Buscar cualquier contenido en Nyaa...", width=280, height=38, font=("Segoe UI", 13)
        )
        self.entry_nyaa_search.pack(side="left", padx=(0, 10))
        self.entry_nyaa_search.bind("<Return>", lambda e: self.reset_page_and_search())

        # Combo Categoría
        self.combo_cat = ctk.CTkComboBox(
            top_frame, values=[
                "Todas las Categorías", 
                "1_0: Anime (Todo)", 
                "1_1: Anime - AMV", 
                "1_2: Anime - English", 
                "1_3: Anime - Non-English (Español)", 
                "1_4: Anime - Raw", 
                "2_0: Audio (Música/OST)", 
                "2_1: Audio - Lossless (FLAC)",
                "2_2: Audio - Lossy (MP3)",
                "3_0: Literatura (Manga)", 
                "3_1: Literatura - English",
                "3_2: Literatura - Non-English",
                "3_3: Literatura - Raw",
                "4_0: Live Action", 
                "5_0: Fotos / Pictures", 
                "6_0: Software / Juegos"
            ], width=220, height=38, command=lambda e: self.reset_page_and_search()
        )
        self.combo_cat.pack(side="left", padx=(0, 10))
        self.combo_cat.set("Todas las Categorías")

        # Combo Filtro Confianza
        self.combo_filter = ctk.CTkComboBox(
            top_frame, values=["0: Sin Filtro", "1: No Remakes", "2: Solo Uploaders Confiables"], width=190, height=38,
            command=lambda e: self.reset_page_and_search()
        )
        self.combo_filter.pack(side="left", padx=(0, 10))

        # Botón Buscar
        btn_search = ctk.CTkButton(
            top_frame, text="🔍 Buscar", font=("Segoe UI", 13, "bold"), height=38, width=100,
            command=self.reset_page_and_search
        )
        btn_search.pack(side="left")

        # Paginación
        self.pagina_actual = 1
        frame_page = ctk.CTkFrame(top_frame, fg_color="transparent")
        frame_page.pack(side="right")

        btn_prev = ctk.CTkButton(frame_page, text="◀", width=32, height=32, command=self.pagina_anterior)
        btn_prev.pack(side="left", padx=2)
        
        self.lbl_page = ctk.CTkLabel(frame_page, text="Pág 1", font=("Segoe UI", 12, "bold"))
        self.lbl_page.pack(side="left", padx=6)

        btn_next = ctk.CTkButton(frame_page, text="▶", width=32, height=32, command=self.pagina_siguiente)
        btn_next.pack(side="left", padx=2)

        # Tabla de Torrents
        frame_tabla = ctk.CTkFrame(self.tab_feed, fg_color="#181B26")
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree_nyaa = ttk.Treeview(
            frame_tabla,
            columns=("Tipo", "Idioma", "Nombre", "Tamaño", "Seeders", "Leechers", "Calidad"),
            show="headings", selectmode="browse"
        )
        self.tree_nyaa.heading("Tipo", text="🏷️ Categoría")
        self.tree_nyaa.heading("Idioma", text="🌐 Idioma")
        self.tree_nyaa.heading("Nombre", text="📄 Título del Torrent")
        self.tree_nyaa.heading("Tamaño", text="📊 Tamaño")
        self.tree_nyaa.heading("Seeders", text="🌱 Seeds")
        self.tree_nyaa.heading("Leechers", text="📉 Leech")
        self.tree_nyaa.heading("Calidad", text="🎬 Calidad")

        self.tree_nyaa.column("Tipo", width=110)
        self.tree_nyaa.column("Idioma", width=120)
        self.tree_nyaa.column("Nombre", width=480)
        self.tree_nyaa.column("Tamaño", width=90)
        self.tree_nyaa.column("Seeders", width=70)
        self.tree_nyaa.column("Leechers", width=70)
        self.tree_nyaa.column("Calidad", width=90)

        scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree_nyaa.yview)
        self.tree_nyaa.configure(yscrollcommand=scrollbar.set)
        
        self.tree_nyaa.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Evento doble clic para ver descripción detallada y traducir
        self.tree_nyaa.bind("<Double-1>", lambda e: self.abrir_detalle_torrent())

        # Barra de acciones inferiores del Feed
        frame_feed_actions = ctk.CTkFrame(self.tab_feed, fg_color="transparent")
        frame_feed_actions.pack(fill="x", padx=10, pady=(0, 5))

        btn_detalles = ctk.CTkButton(
            frame_feed_actions, text="📖 Ver Detalles y Descripción", font=("Segoe UI", 12, "bold"),
            fg_color="#3B82F6", hover_color="#2563EB", height=34, command=self.abrir_detalle_torrent
        )
        btn_detalles.pack(side="left", padx=(0, 10))

        btn_dl_feed = ctk.CTkButton(
            frame_feed_actions, text="⬇️ Descargar / Magnet", font=("Segoe UI", 12, "bold"),
            fg_color="#10B981", hover_color="#059669", height=34, command=self.descargar_o_abrir_seleccion
        )
        btn_dl_feed.pack(side="left", padx=(0, 10))

        btn_fav_feed = ctk.CTkButton(
            frame_feed_actions, text="⭐ Guardar Favorito", font=("Segoe UI", 12),
            fg_color="#F59E0B", hover_color="#D97706", height=34, command=self.guardar_seleccion_favorito
        )
        btn_fav_feed.pack(side="left")

    def obtener_torrent_seleccionado(self):
        sel = self.tree_nyaa.selection()
        if not sel:
            messagebox.showinfo("Selección requerida", "Selecciona un torrent de la lista.")
            return None
        idx = self.tree_nyaa.index(sel[0])
        if idx < len(self.torrents_filtrados):
            return self.torrents_filtrados[idx]
        return None

    def abrir_detalle_torrent(self, torrent=None):
        """Abre un modal con la descripción completa del torrent e incluye traductor multilingüe."""
        if not torrent:
            torrent = self.obtener_torrent_seleccionado()
        if not torrent:
            return

        modal = ctk.CTkToplevel(self.window)
        modal.title(f"📖 Detalles: {torrent['nombre'][:50]}...")
        modal.geometry("880x680")
        modal.grab_set()

        # Cabecera
        lbl_title = ctk.CTkLabel(modal, text=f"{torrent['emoji']} {torrent['nombre']}", font=("Segoe UI", 15, "bold"), wraplength=820, justify="left")
        lbl_title.pack(anchor="w", padx=20, pady=(15, 5))

        # Metadatos
        meta_str = f"🏷️ Categoría: {torrent['tipo']}  |  📊 Tamaño: {torrent['tamano']}  |  🌱 Seeds: {torrent['seeders']}  |  📉 Leech: {torrent['leechers']}"
        ctk.CTkLabel(modal, text=meta_str, font=("Segoe UI", 11), text_color="#9CA3AF").pack(anchor="w", padx=20, pady=(0, 10))

        # BARRA DE TRADUCCIÓN
        f_trans = ctk.CTkFrame(modal, fg_color="#1F2330", corner_radius=6)
        f_trans.pack(fill="x", padx=20, pady=(0, 10))

        ctk.CTkLabel(f_trans, text="🌐 Traducir descripción a:", font=("Segoe UI", 12, "bold")).pack(side="left", padx=10, pady=8)

        combo_idioma = ctk.CTkComboBox(f_trans, values=list(IDIOMAS_TRADUCCION.keys()), width=180, height=32)
        combo_idioma.pack(side="left", padx=5, pady=8)
        combo_idioma.set("Español")

        # Textbox para la descripción
        txt_desc = ctk.CTkTextbox(modal, font=("Segoe UI", 12), wrap="word")
        txt_desc.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        txt_desc.insert("1.0", "⏳ Cargando descripción original desde Nyaa.si...")

        def _do_translate():
            target_lang_name = combo_idioma.get()
            target_code = IDIOMAS_TRADUCCION.get(target_lang_name, 'es')
            
            original_text = txt_desc.get("1.0", "end-1c")
            if not original_text or "Cargando" in original_text:
                return

            self.lbl_status.configure(text=f"🌐 Traduciendo descripción a {target_lang_name}...")
            
            def _th():
                traducido = traducir_texto(original_text, target_code)
                modal.after(0, lambda: txt_desc.delete("1.0", "end"))
                modal.after(0, lambda: txt_desc.insert("1.0", traducido))
                modal.after(0, lambda: self.lbl_status.configure(text="✅ Traducción completada."))

            threading.Thread(target=_th, daemon=True).start()

        btn_trans = ctk.CTkButton(
            f_trans, text="🌐 Traducir Ahora", font=("Segoe UI", 12, "bold"),
            fg_color="#8B5CF6", hover_color="#7C3AED", height=32, command=_do_translate
        )
        btn_trans.pack(side="left", padx=10, pady=8)

        # Botones de Acción
        f_btns = ctk.CTkFrame(modal, fg_color="transparent")
        f_btns.pack(fill="x", padx=20, pady=(0, 15))

        if torrent.get('magnet'):
            ctk.CTkButton(
                f_btns, text="🧲 Abrir Magnet", font=("Segoe UI", 12, "bold"), fg_color="#10B981",
                command=lambda: abrir_recurso(torrent['magnet'])
            ).pack(side="left", padx=(0, 10))

        if torrent.get('enlace'):
            ctk.CTkButton(
                f_btns, text="⬇️ Descargar .Torrent", font=("Segoe UI", 12),
                command=lambda: abrir_recurso(torrent['enlace'])
            ).pack(side="left", padx=(0, 10))

        if torrent.get('view_url'):
            ctk.CTkButton(
                f_btns, text="🔗 Abrir en Nyaa.si", font=("Segoe UI", 12), fg_color="#3B82F6",
                command=lambda: abrir_recurso(torrent['view_url'])
            ).pack(side="left")

        # Cargar contenido HTML/Markdown formateado desde Nyaa
        def _fetch_desc():
            if not torrent.get('view_url'):
                modal.after(0, lambda: txt_desc.delete("1.0", "end"))
                modal.after(0, lambda: txt_desc.insert("1.0", "No se encontró enlace de descripción para este torrent."))
                return

            try:
                res = requests.get(torrent['view_url'], headers=HEADERS, timeout=12)
                soup = BeautifulSoup(res.text, 'html.parser')
                desc_div = soup.find('div', id='torrent-description')
                
                desc_text = desc_div.text.strip() if desc_div else "Sin descripción provista por el uploader."
                
                modal.after(0, lambda: txt_desc.delete("1.0", "end"))
                modal.after(0, lambda: txt_desc.insert("1.0", desc_text))
            except Exception as e:
                modal.after(0, lambda: txt_desc.delete("1.0", "end"))
                modal.after(0, lambda: txt_desc.insert("1.0", f"Error al descargar descripción: {e}"))

        threading.Thread(target=_fetch_desc, daemon=True).start()

    def reset_page_and_search(self):
        """Reinicia la página a 1 y realiza la búsqueda con la categoría/filtro seleccionados."""
        self.pagina_actual = 1
        if hasattr(self, 'lbl_page'):
            self.lbl_page.configure(text=f"Pág {self.pagina_actual}")
        self.cargar_feed_nyaa()

    def pagina_anterior(self):
        if self.pagina_actual > 1:
            self.pagina_actual -= 1
            self.lbl_page.configure(text=f"Pág {self.pagina_actual}")
            self.cargar_feed_nyaa()

    def pagina_siguiente(self):
        self.pagina_actual += 1
        self.lbl_page.configure(text=f"Pág {self.pagina_actual}")
        self.cargar_feed_nyaa()

    def cargar_feed_nyaa(self):
        """Descarga e interpreta el feed de torrents desde Nyaa.si."""
        q = self.entry_nyaa_search.get().strip()
        
        cat_raw = self.combo_cat.get()
        if "Todas" in cat_raw:
            cat = "0_0"
        elif ":" in cat_raw:
            cat = cat_raw.split(":")[0].strip()
        else:
            cat = "0_0"

        f_val = self.combo_filter.get().split(":")[0].strip() if ":" in self.combo_filter.get() else "0"

        params = {'f': f_val, 'c': cat, 'q': q, 'p': self.pagina_actual}
        url = "https://nyaa.si/?" + urllib.parse.urlencode(params)

        self.lbl_status.configure(text=f"⏳ Cargando feed Nyaa (Categoría: {cat}, Página {self.pagina_actual})...")

        def _fetch():
            try:
                res = requests.get(url, headers=HEADERS, timeout=15)
                res.raise_for_status()
                soup = BeautifulSoup(res.text, 'html.parser')

                torrents = []
                rows = soup.find_all('tr', class_=re.compile(r'(default|success|danger)'))

                for r in rows:
                    cols = r.find_all('td')
                    if len(cols) < 6:
                        continue

                    # Tipo badge
                    cat_a = cols[0].find('a')
                    tipo_badge = cat_a.get('title', 'General') if cat_a else 'General'

                    # Título y view url
                    name_links = cols[1].find_all('a')
                    title = name_links[-1].text.strip() if name_links else "Sin título"
                    view_href = name_links[-1].get('href', '') if name_links else ''
                    view_url = ("https://nyaa.si" + view_href) if view_href.startswith('/view/') else None

                    # Magnet y Torrent
                    torrent_link, magnet_link = None, None
                    for a in cols[2].find_all('a'):
                        href = a.get('href', '')
                        if href.startswith('/download/'):
                            torrent_link = "https://nyaa.si" + href
                        elif href.startswith('magnet:'):
                            magnet_link = href

                    if not torrent_link and not magnet_link:
                        continue

                    idioma, emoji, color = detectar_idioma_torrent(title)
                    calidad = detectar_calidad(title)

                    size = cols[3].text.strip()
                    seeds = cols[5].text.strip() if len(cols) > 5 else "0"
                    leech = cols[6].text.strip() if len(cols) > 6 else "0"

                    torrents.append({
                        'tipo': tipo_badge, 'nombre': title, 'tamano': size, 'seeders': seeds,
                        'leechers': leech, 'calidad': calidad, 'enlace': torrent_link,
                        'magnet': magnet_link, 'view_url': view_url, 'idioma': idioma,
                        'emoji': emoji, 'color': color,
                        'filename': torrent_link.split('/')[-1] if torrent_link else "download.torrent"
                    })

                self.torrents_lista = torrents
                self.torrents_filtrados = torrents.copy()

                self.window.after(0, self.actualizar_tabla_feed)
                self.window.after(0, lambda: self.lbl_status.configure(
                    text=f"✅ Cargados {len(torrents)} torrents desde Nyaa.si"
                ))
            except Exception as e:
                self.window.after(0, lambda: self.lbl_status.configure(text=f"❌ Error al cargar Nyaa: {e}"))

        threading.Thread(target=_fetch, daemon=True).start()

    def actualizar_tabla_feed(self):
        for item in self.tree_nyaa.get_children():
            self.tree_nyaa.delete(item)

        for t in self.torrents_filtrados:
            idioma_str = f"{t['emoji']} {t['idioma']}"
            self.tree_nyaa.insert("", "end", values=(
                t['tipo'], idioma_str, t['nombre'], t['tamano'], t['seeders'], t['leechers'], t['calidad']
            ))

    def crear_tab_anilist(self):
        top_frame = ctk.CTkFrame(self.tab_anilist, fg_color="transparent")
        top_frame.pack(fill="x", padx=10, pady=10)

        self.entry_anilist = ctk.CTkEntry(
            top_frame, placeholder_text="Buscar en AniList (ej: 'Shingeki no Kyojin', 'One Piece')...",
            width=450, height=38, font=("Segoe UI", 13)
        )
        self.entry_anilist.pack(side="left", padx=(0, 10))
        self.entry_anilist.bind("<Return>", lambda e: self.buscar_anilist())

        btn = ctk.CTkButton(
            top_frame, text="🔍 Buscar Anime", font=("Segoe UI", 13, "bold"), height=38,
            command=self.buscar_anilist
        )
        btn.pack(side="left")

        # Scrollable Frame para tarjetas de Anime
        self.scroll_anilist = ctk.CTkScrollableFrame(self.tab_anilist, fg_color="#12141D")
        self.scroll_anilist.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def buscar_anilist(self):
        q = self.entry_anilist.get().strip()
        if not q:
            return

        self.lbl_status.configure(text=f"🔍 Consultando AniList API para '{q}'...")
        for w in self.scroll_anilist.winfo_children():
            w.destroy()

        def _search():
            query = """
            query ($search: String) {
              Page(page: 1, perPage: 10) {
                media(search: $search, type: ANIME, isAdult: false) {
                  id
                  title { romaji english native }
                  coverImage { large }
                  description
                  averageScore
                  episodes
                  genres
                }
              }
            }
            """
            try:
                res = requests.post(
                    'https://graphql.anilist.co', json={'query': query, 'variables': {'search': q}},
                    headers=HEADERS, timeout=12
                )
                data = res.json().get('data', {}).get('Page', {}).get('media', [])
                self.window.after(0, lambda: self.renderizar_cartas_anilist(data))
            except Exception as e:
                self.window.after(0, lambda: self.lbl_status.configure(text=f"❌ Error AniList: {e}"))

        threading.Thread(target=_search, daemon=True).start()

    def renderizar_cartas_anilist(self, animes):
        if not animes:
            ctk.CTkLabel(self.scroll_anilist, text="No se encontraron resultados.", font=("Segoe UI", 14)).pack(pady=20)
            return

        for a in animes:
            card = ctk.CTkFrame(self.scroll_anilist, fg_color="#1F2330", corner_radius=10)
            card.pack(fill="x", padx=5, pady=6)

            title = a.get('title', {}).get('english') or a.get('title', {}).get('romaji') or "Sin Título"
            score = a.get('averageScore', 0)
            eps = a.get('episodes', '?')
            desc_raw = re.sub(r'<[^>]+>', '', a.get('description', 'Sin sinopsis disponibles.'))

            lbl_title = ctk.CTkLabel(card, text=f"🎬 {title}", font=("Segoe UI", 15, "bold"), text_color="#3B82F6")
            lbl_title.pack(anchor="w", padx=12, pady=(10, 2))

            lbl_meta = ctk.CTkLabel(
                card, text=f"⭐ Puntuación: {score}/100 | 📺 Episodios: {eps} | 🏷️ {', '.join(a.get('genres', [])[:3])}",
                font=("Segoe UI", 11), text_color="#9CA3AF"
            )
            lbl_meta.pack(anchor="w", padx=12, pady=(0, 4))

            lbl_desc = ctk.CTkLabel(card, text=desc_raw[:300] + "...", font=("Segoe UI", 11), text_color="#D1D5DB", wraplength=800, justify="left")
            lbl_desc.pack(anchor="w", padx=12, pady=(0, 10))

            f_card_actions = ctk.CTkFrame(card, fg_color="transparent")
            f_card_actions.pack(fill="x", padx=12, pady=(0, 10))

            btn_find = ctk.CTkButton(
                f_card_actions, text=f"🔎 Buscar Torrents", font=("Segoe UI", 11, "bold"), height=28,
                command=lambda t=title: self.buscar_torrents_desde_card(t)
            )
            btn_find.pack(side="left")

            def _translate_synopsis(label_widget=lbl_desc, full_text=desc_raw):
                def _th():
                    self.lbl_status.configure(text=f"🌐 Traduciendo sinopsis de '{title[:20]}...'")
                    tr = traducir_texto(full_text, 'es')
                    label_widget.configure(text=tr)
                    self.lbl_status.configure(text="✅ Sinopsis traducida al español.")
                threading.Thread(target=_th, daemon=True).start()

            btn_tr = ctk.CTkButton(
                f_card_actions, text="🌐 Traducir Sinopsis (Español)", font=("Segoe UI", 11),
                fg_color="#8B5CF6", hover_color="#7C3AED", height=28, command=_translate_synopsis
            )
            btn_tr.pack(side="right")

        self.lbl_status.configure(text=f"✅ Encontrados {len(animes)} resultados en AniList")

    def buscar_torrents_desde_card(self, titulo):
        self.entry_nyaa_search.delete(0, "end")
        self.entry_nyaa_search.insert(0, titulo)
        self.mostrar_tab_feed()
        self.cargar_feed_nyaa()

    def crear_tab_upload(self):
        container = ctk.CTkScrollableFrame(self.tab_upload, fg_color="#12141D")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        lbl_t = ctk.CTkLabel(container, text="📤 Publicar Torrent en Nyaa.si", font=("Segoe UI", 18, "bold"))
        lbl_t.pack(anchor="w", padx=10, pady=10)

        # Selección de archivo torrent
        f_file = ctk.CTkFrame(container, fg_color="#1A1D27")
        f_file.pack(fill="x", padx=10, pady=5)

        self.entry_torrent_path = ctk.CTkEntry(f_file, placeholder_text="Selecciona tu archivo .torrent local...", font=("Segoe UI", 12))
        self.entry_torrent_path.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        btn_browse = ctk.CTkButton(f_file, text="📁 Examinar", width=100, command=self.examinar_torrent_local)
        btn_browse.pack(side="right", padx=10, pady=10)

        # Nombre del torrent
        ctk.CTkLabel(container, text="📌 Título del Torrent:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        self.entry_upload_title = ctk.CTkEntry(container, placeholder_text="Ej: [MiGrupo] Mi Anime - 01 [1080p HEVC Multi-Sub]", font=("Segoe UI", 12))
        self.entry_upload_title.pack(fill="x", padx=10, pady=(0, 10))

        # Categoría
        ctk.CTkLabel(container, text="🏷️ Categoría Nyaa:", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=(5, 2))
        self.combo_upload_cat = ctk.CTkComboBox(
            container, values=[
                "1_1: Anime - AMV", 
                "1_2: Anime - English-translated", 
                "1_3: Anime - Non-English-translated (Español)", 
                "1_4: Anime - Raw",
                "2_1: Audio - Lossless", 
                "2_2: Audio - Lossy", 
                "3_1: Literatura - English-translated", 
                "3_2: Literatura - Non-English-translated",
                "3_3: Literatura - Raw",
                "4_1: Live Action - English-translated", 
                "4_2: Live Action - Idol/PV",
                "4_3: Live Action - Non-English-translated",
                "4_4: Live Action - Raw",
                "5_1: Pictures - Graphics",
                "5_2: Pictures - Photos",
                "6_1: Software - Applications",
                "6_2: Software - Games"
            ], width=350, height=38
        )
        self.combo_upload_cat.pack(fill="x", padx=10, pady=(0, 10))
        self.combo_upload_cat.set("1_3: Anime - Non-English-translated (Español)")

        # Website / Info link
        ctk.CTkLabel(container, text="🔗 Enlace Web de Información (Opcional):", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=(5, 2))
        self.entry_upload_url = ctk.CTkEntry(container, placeholder_text="https://", font=("Segoe UI", 12))
        self.entry_upload_url.pack(fill="x", padx=10, pady=(0, 10))

        # Opciones Checkbox
        f_checks = ctk.CTkFrame(container, fg_color="transparent")
        f_checks.pack(fill="x", padx=10, pady=5)

        self.var_anon = ctk.BooleanVar(value=False)
        self.var_remake = ctk.BooleanVar(value=False)
        self.var_hidden = ctk.BooleanVar(value=False)

        ctk.CTkCheckBox(f_checks, text="👤 Subir como Anónimo", variable=self.var_anon).pack(side="left", padx=(0, 15))
        ctk.CTkCheckBox(f_checks, text="🔄 Marcar como Remake", variable=self.var_remake).pack(side="left", padx=(0, 15))
        ctk.CTkCheckBox(f_checks, text="🙈 Ocultar del Índice", variable=self.var_hidden).pack(side="left")

        # Descripción
        ctk.CTkLabel(container, text="📖 Descripción (Markdown / Texto):", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=(10, 2))
        self.txt_upload_desc = ctk.CTkTextbox(container, height=180, font=("Segoe UI", 12))
        self.txt_upload_desc.pack(fill="x", padx=10, pady=(0, 15))

        # Botón Subir
        btn_submit = ctk.CTkButton(
            container, text="🚀 Publicar Torrent en Nyaa.si", font=("Segoe UI", 14, "bold"),
            fg_color="#10B981", hover_color="#059669", height=42, command=self.ejecutar_upload_nyaa
        )
        btn_submit.pack(fill="x", padx=10, pady=10)

    def examinar_torrent_local(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo Torrent", filetypes=[("Archivos Torrent", "*.torrent")]
        )
        if filename:
            self.entry_torrent_path.delete(0, "end")
            self.entry_torrent_path.insert(0, filename)
            if not self.entry_upload_title.get():
                base = os.path.basename(filename).replace(".torrent", "")
                self.entry_upload_title.insert(0, base)

    def ejecutar_upload_nyaa(self):
        if not self.usuario_logueado:
            messagebox.showerror("Inicia Sesión", "Debes estar conectado a tu cuenta de Nyaa.")
            return

        torrent_path = self.entry_torrent_path.get().strip()
        title = self.entry_upload_title.get().strip()
        cat = self.combo_upload_cat.get().split(":")[0].strip()

        if not os.path.exists(torrent_path):
            messagebox.showwarning("Archivo faltante", "Selecciona un archivo .torrent válido.")
            return

        if not title:
            messagebox.showwarning("Título requerido", "Ingresa el nombre para el torrent.")
            return

        self.lbl_status.configure(text="⏳ Enviando torrent a Nyaa.si...")

        def _upload():
            try:
                # 1. Obtener Token CSRF del formulario /upload
                get_res = self.session.get("https://nyaa.si/upload", timeout=12)
                soup = BeautifulSoup(get_res.text, 'html.parser')
                csrf_input = soup.find('input', {'name': 'csrf_token'})
                csrf_token = csrf_input.get('value') if csrf_input else ""

                if not csrf_token:
                    raise Exception("No se pudo obtener el token de seguridad CSRF de Nyaa.")

                # 2. Formatear datos multipart/form-data
                data = {
                    'csrf_token': csrf_token,
                    'torrent_name': title,
                    'category': cat,
                    'information': self.entry_upload_url.get().strip(),
                    'description': self.txt_upload_desc.get("1.0", "end-1c"),
                }

                if self.var_anon.get():
                    data['anonymous'] = 'on'
                if self.var_remake.get():
                    data['remake'] = 'on'
                if self.var_hidden.get():
                    data['hidden'] = 'on'

                with open(torrent_path, 'rb') as f:
                    files = {'torrent_file': (os.path.basename(torrent_path), f, 'application/x-bittorrent')}
                    post_res = self.session.post("https://nyaa.si/upload", data=data, files=files, timeout=20)

                if post_res.status_code == 200 and "/view/" in post_res.url:
                    self.window.after(0, lambda: messagebox.showinfo(
                        "✅ Éxito", f"¡Torrent publicado con éxito!\n\nVer enlace:\n{post_res.url}"
                    ))
                    self.window.after(0, lambda: abrir_recurso(post_res.url))
                    self.window.after(0, lambda: self.lbl_status.configure(text="✅ Torrent subido correctamente."))
                else:
                    soup_err = BeautifulSoup(post_res.text, 'html.parser')
                    err_msg = soup_err.find('div', class_='alert-danger')
                    err_txt = err_msg.text.strip() if err_msg else "Error desconocido al procesar la solicitud."
                    raise Exception(f"Nyaa rechazó la subida: {err_txt}")

            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("❌ Error al Subir", str(e)))
                self.window.after(0, lambda: self.lbl_status.configure(text=f"❌ Falló la subida: {e}"))

        threading.Thread(target=_upload, daemon=True).start()

    def abrir_dialogo_login(self):
        if self.usuario_logueado:
            if messagebox.askyesno("Cerrar Sesión", "¿Deseas cerrar la sesión activa?"):
                self.session.cookies.clear()
                self.guardar_cookies_sesion()
                self.comprobar_estado_usuario()
            return

        dialog = ctk.CTkToplevel(self.window)
        dialog.title("🔑 Iniciar Sesión en Nyaa.si")
        dialog.geometry("380x300")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="🔑 Conectar Cuenta Nyaa", font=("Segoe UI", 16, "bold")).pack(pady=(20, 15))

        entry_user = ctk.CTkEntry(dialog, placeholder_text="Usuario o Email", width=280)
        entry_user.pack(pady=8)

        entry_pass = ctk.CTkEntry(dialog, placeholder_text="Contraseña", show="*", width=280)
        entry_pass.pack(pady=8)

        def _do_login():
            user = entry_user.get().strip()
            password = entry_pass.get().strip()

            if not user or not password:
                messagebox.showwarning("Incompleto", "Ingresa usuario y contraseña.")
                return

            try:
                res_get = self.session.get("https://nyaa.si/login", timeout=10)
                soup = BeautifulSoup(res_get.text, 'html.parser')
                csrf = soup.find('input', {'name': 'csrf_token'})
                csrf_token = csrf.get('value') if csrf else ""

                post_data = {
                    'csrf_token': csrf_token,
                    'username': user,
                    'password': password
                }

                res_post = self.session.post("https://nyaa.si/login", data=post_data, timeout=12)

                if "Invalid username or password" in res_post.text:
                    messagebox.showerror("Error Login", "Usuario o contraseña incorrectos en Nyaa.si.")
                else:
                    self.guardar_cookies_sesion()
                    self.comprobar_estado_usuario()
                    dialog.destroy()
                    messagebox.showinfo("✅ Sesión Iniciada", f"¡Bienvenido de nuevo!")
            except Exception as e:
                messagebox.showerror("Error de Red", f"No se pudo iniciar sesión: {e}")

        btn = ctk.CTkButton(dialog, text="Entrar", font=("Segoe UI", 13, "bold"), command=_do_login, width=280, height=36)
        btn.pack(pady=20)

    def crear_tab_favs(self):
        self.scroll_favs = ctk.CTkScrollableFrame(self.tab_favs, fg_color="#12141D")
        self.scroll_favs.pack(fill="both", expand=True, padx=10, pady=10)

    def cargar_favoritos(self):
        if os.path.exists(self.file_favs):
            try:
                with open(self.file_favs, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def guardar_favoritos_disco(self):
        try:
            with open(self.file_favs, 'w', encoding='utf-8') as f:
                json.dump(self.favoritos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando favs: {e}")

    def guardar_seleccion_favorito(self):
        t = self.obtener_torrent_seleccionado()
        if not t:
            return
        if any(f['nombre'] == t['nombre'] for f in self.favoritos):
            messagebox.showinfo("Favoritos", "Este torrent ya está guardado en tus favoritos.")
            return

        self.favoritos.append(t)
        self.guardar_favoritos_disco()
        self.lbl_status.configure(text=f"⭐ Guardado en favoritos: {t['nombre'][:40]}...")

    def actualizar_vista_favoritos(self):
        for w in self.scroll_favs.winfo_children():
            w.destroy()

        if not self.favoritos:
            ctk.CTkLabel(self.scroll_favs, text="⭐ No tienes torrents guardados en favoritos.", font=("Segoe UI", 14)).pack(pady=30)
            return

        for i, fav in enumerate(self.favoritos):
            f = ctk.CTkFrame(self.scroll_favs, fg_color="#1F2330", corner_radius=8)
            f.pack(fill="x", padx=5, pady=4)

            lbl = ctk.CTkLabel(f, text=f"{fav['emoji']} {fav['nombre']}", font=("Segoe UI", 12, "bold"), text_color="#F3F4F6")
            lbl.pack(side="left", padx=10, pady=8)

            btn_rem = ctk.CTkButton(f, text="🗑️", width=30, height=28, fg_color="#EF4444", command=lambda idx=i: self.borrar_favorito(idx))
            btn_rem.pack(side="right", padx=10)

            if fav.get('magnet'):
                btn_mag = ctk.CTkButton(f, text="🧲 Magnet", width=80, height=28, command=lambda m=fav['magnet']: abrir_recurso(m))
                btn_mag.pack(side="right", padx=5)

    def borrar_favorito(self, idx):
        if idx < len(self.favoritos):
            self.favoritos.pop(idx)
            self.guardar_favoritos_disco()
            self.actualizar_vista_favoritos()

    def crear_tab_downloads(self):
        f = ctk.CTkFrame(self.tab_downloads, fg_color="transparent")
        f.pack(fill="both", expand=True, padx=10, pady=10)

        lbl = ctk.CTkLabel(f, text="📥 Gestor de Descargas Activas", font=("Segoe UI", 16, "bold"))
        lbl.pack(anchor="w", pady=(0, 10))

        self.scroll_dl = ctk.CTkScrollableFrame(f, fg_color="#12141D")
        self.scroll_dl.pack(fill="both", expand=True, pady=(0, 10))

        btn_folder = ctk.CTkButton(
            f, text="📂 Abrir Carpeta de Descargas", font=("Segoe UI", 13), height=38,
            command=lambda: abrir_recurso(self.dir_descargas)
        )
        btn_folder.pack(anchor="w")

    # =========================================================
    # NUEVA LÓGICA DE DESCARGA (soporta .torrent y magnet)
    # =========================================================
    def descargar_o_abrir_seleccion(self):
        """
        Descarga el contenido del torrent usando Transmission o aria2 si están disponibles.
        Soporta tanto enlaces a archivos .torrent como enlaces magnet.
        """
        t = self.obtener_torrent_seleccionado()
        if not t:
            return

        url = t.get('enlace') or t.get('magnet')
        if not url:
            messagebox.showwarning("Sin enlace", "Este torrent no tiene enlace de descarga ni magnet disponible.")
            return

        # Si hay un cliente disponible, usar descarga automática
        if self.transmission_disponible or self.aria2_disponible:
            self.descargar_con_cliente(t)
        else:
            # Si no hay cliente, abrir la URL con el sistema
            abrir_recurso(url)
            self.lbl_status.configure(text="📄 Enlace abierto. Usa tu cliente BitTorrent para continuar.")
            messagebox.showinfo(
                "Cliente BitTorrent no encontrado",
                "No se encontró Transmission ni aria2 en tu sistema.\n\n"
                "Se ha abierto el enlace (magnet o .torrent) en tu navegador.\n"
                "Descárgalo y ábrelo con tu cliente BitTorrent favorito."
            )

    def descargar_con_cliente(self, torrent):
        """
        Elige el cliente disponible (aria2 preferido por ser más fiable) y lanza la descarga.
        """
        url = torrent.get('enlace') or torrent.get('magnet')
        if not url:
            return

        nombre = torrent.get('nombre', 'Torrent')

        # Priorizar aria2 porque siempre espera a que termine la descarga
        if self.aria2_disponible:
            self.descargar_con_aria2(url, nombre)
        elif self.transmission_disponible:
            self.descargar_con_transmission(url, nombre)
        else:
            # No debería llegar aquí, pero por si acaso
            abrir_recurso(url)

    def descargar_con_transmission(self, url, nombre):
        """
        Descarga usando transmission-cli con la opción --exit para que espere a que termine.
        Si url es un enlace http, descarga el archivo .torrent;
        si es un magnet, lo pasa directamente.
        """
        def _dl():
            try:
                if url.startswith('magnet:'):
                    # Es un magnet, usarlo directamente
                    cmd = ['transmission-cli', '--exit', '-w', self.dir_descargas, url]
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"🧲 Descargando magnet con Transmission: {nombre[:30]}..."
                    ))
                else:
                    # Es un enlace a .torrent, descargar el archivo primero
                    r = requests.get(url, headers=HEADERS, timeout=15)
                    nombre_archivo = f"temp_{int(time.time())}.torrent"
                    tmp_path = os.path.join(self.dir_descargas, nombre_archivo)
                    with open(tmp_path, 'wb') as f:
                        f.write(r.content)
                    cmd = ['transmission-cli', '--exit', '-w', self.dir_descargas, tmp_path]
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"⬇️ Descargando con Transmission: {nombre[:30]}..."
                    ))

                # Ejecutar y esperar (timeout de 1 hora)
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

                if result.returncode == 0:
                    self.window.after(0, lambda: self.mostrar_notificacion_descarga_completa(nombre))
                else:
                    error_msg = result.stderr.strip() or "Código de error desconocido."
                    self.window.after(0, lambda: messagebox.showerror(
                        "Error en Transmission",
                        f"Transmission finalizó con código {result.returncode}.\n\nDetalles:\n{error_msg}"
                    ))
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"❌ Falló la descarga de {nombre[:30]}..."
                    ))

            except subprocess.TimeoutExpired:
                self.window.after(0, lambda: messagebox.showerror(
                    "Timeout",
                    "La descarga ha excedido el tiempo límite (1 hora). Puede que no haya seeds suficientes."
                ))
                self.window.after(0, lambda: self.lbl_status.configure(text="⏰ Tiempo de descarga agotado"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Error Transmission", str(e)))
                self.window.after(0, lambda: self.lbl_status.configure(text="❌ Error en la descarga"))

        threading.Thread(target=_dl, daemon=True).start()

    def descargar_con_aria2(self, url, nombre):
        """
        Descarga usando aria2c. Acepta magnet o enlace a .torrent.
        aria2c siempre espera a que termine la descarga.
        """
        def _dl():
            try:
                if url.startswith('magnet:'):
                    cmd = ['aria2c', '--seed-time=0', '--dir=' + self.dir_descargas, url]
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"🧲 Descargando magnet con aria2: {nombre[:30]}..."
                    ))
                else:
                    r = requests.get(url, headers=HEADERS, timeout=15)
                    nombre_archivo = f"temp_{int(time.time())}.torrent"
                    tmp_path = os.path.join(self.dir_descargas, nombre_archivo)
                    with open(tmp_path, 'wb') as f:
                        f.write(r.content)
                    cmd = ['aria2c', '--seed-time=0', '--dir=' + self.dir_descargas, tmp_path]
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"⬇️ Descargando con aria2: {nombre[:30]}..."
                    ))

                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)

                if result.returncode == 0:
                    self.window.after(0, lambda: self.mostrar_notificacion_descarga_completa(nombre))
                else:
                    error_msg = result.stderr.strip() or "Código de error desconocido."
                    self.window.after(0, lambda: messagebox.showerror(
                        "Error en aria2",
                        f"aria2c finalizó con código {result.returncode}.\n\nDetalles:\n{error_msg}"
                    ))
                    self.window.after(0, lambda: self.lbl_status.configure(
                        text=f"❌ Falló la descarga de {nombre[:30]}..."
                    ))

            except subprocess.TimeoutExpired:
                self.window.after(0, lambda: messagebox.showerror(
                    "Timeout",
                    "La descarga ha excedido el tiempo límite (1 hora). Puede que no haya seeds suficientes."
                ))
                self.window.after(0, lambda: self.lbl_status.configure(text="⏰ Tiempo de descarga agotado"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("Error aria2", str(e)))
                self.window.after(0, lambda: self.lbl_status.configure(text="❌ Error en la descarga"))

        threading.Thread(target=_dl, daemon=True).start()

    def mostrar_notificacion_descarga_completa(self, nombre):
        """
        Muestra una ventana emergente y actualiza la barra de estado
        cuando la descarga del contenido ha finalizado con éxito.
        """
        self.lbl_status.configure(text=f"✅ Descarga completada: {nombre[:40]}...")
        messagebox.showinfo(
            "📥 Descarga finalizada",
            f"El contenido del torrent '{nombre}' se ha descargado correctamente.\n\n"
            f"📂 Carpeta: {self.dir_descargas}"
        )

if __name__ == "__main__":
    try:
        app = NyaaDesktopApp()
    except KeyboardInterrupt:
        sys.exit(0)
