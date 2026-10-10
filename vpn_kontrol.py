"""
VPN / Sansür Kontrol
====================
IP adresinizi sorgular, konumunuzu haritada gösterir ve IP'nin
Türkiye'den gelip gelmediğini kontrol ederek VPN'in çalışıp
çalışmadığını anlamanızı sağlar. Aydınlık / Karanlık / Sistem teması
desteklenir ve seçiminiz hatırlanır.

Çalıştırma:
    python vpn_kontrol.py
"""

import os
import sys
import json
import threading

import requests
import customtkinter as ctk

# Harita kütüphanesi kurulu değilse program yine de çalışsın (harita hariç).
try:
    from tkintermapview import TkinterMapView
    MAP_AVAILABLE = True
except Exception:
    MAP_AVAILABLE = False

# --- Dosya yolları (hem script hem .exe içinde çalışsın) ---
if getattr(sys, "frozen", False):          # PyInstaller ile paketlendiğinde
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_ICO = os.path.join(BASE_DIR, "logo.ico")
LOGO_LIGHT = os.path.join(BASE_DIR, "logo_light.png")
LOGO_DARK = os.path.join(BASE_DIR, "logo_dark.png")
CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".vpn_kontrol.json")

# Ücretsiz, API anahtarı gerektirmeyen IP sorgulama servisi.
API_URL = "http://ip-api.com/json/"
TURKEY_CODE = "TR"

# Harita tile sunucuları (hafif ve hızlı: CartoDB)
TILE_LIGHT = "https://a.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
TILE_DARK = "https://a.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png"

# Durum renkleri
RENK_TURKIYE = "#c0392b"   # kırmızı
RENK_DISI = "#27ae60"      # yeşil
RENK_BEKLE = "#555555"     # gri
RENK_HATA = "#aa0000"      # koyu kırmızı


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(cfg):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


class VPNKontrolApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode(self.cfg.get("appearance", "System"))

        self.title("VPN Kontrol – Sansür Kontrol")
        self.geometry("470x740")
        self.minsize(430, 700)

        # Pencere / görev çubuğu simgesi
        try:
            if os.path.exists(LOGO_ICO):
                self.iconbitmap(default=LOGO_ICO)
        except Exception:
            pass

        self._build_widgets()
        self._apply_map_theme()
        # Açılışta otomatik kontrol
        self.check_ip()

    # ------------------------------------------------------------------ UI
    def _build_widgets(self):
        # Üst satır: logo + başlık + tema seçici
        ust = ctk.CTkFrame(self, fg_color="transparent")
        ust.pack(fill="x", padx=14, pady=(12, 4))
        try:
            from PIL import Image
            light = Image.open(LOGO_LIGHT)
            dark = Image.open(LOGO_DARK)
            self._logo = ctk.CTkImage(light_image=light, dark_image=dark, size=(48, 48))
            ctk.CTkLabel(ust, image=self._logo, text="").pack(side="left", padx=(0, 10))
        except Exception:
            pass
        ctk.CTkLabel(ust, text="VPN / Sansür Kontrol",
                     font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        self.tema_menu = ctk.CTkOptionMenu(
            ust, values=["Aydınlık", "Karanlık", "Sistem"],
            command=self._change_theme, width=110)
        self.tema_menu.pack(side="right")
        self._set_menu_value()

        # Durum bandı (VPN çalışıyor mu?)
        self.status = ctk.CTkLabel(self, text="Kontrol ediliyor...",
                                   font=ctk.CTkFont(size=13, weight="bold"),
                                   text_color="white", fg_color=RENK_BEKLE,
                                   corner_radius=8, wraplength=400,
                                   justify="center", padx=10, pady=10)
        self.status.pack(fill="x", padx=14, pady=6)

        # Bağlantı bilgileri
        info = ctk.CTkFrame(self)
        info.pack(fill="x", padx=14, pady=6)
        self.info_labels = {}
        satirlar = ["IP Adresi", "Ülke", "Bölge / Şehir", "Sağlayıcı (ISP)", "Koordinatlar"]
        for i, anahtar in enumerate(satirlar):
            ctk.CTkLabel(info, text=anahtar + ":", anchor="w",
                         font=ctk.CTkFont(size=12, weight="bold")).grid(
                row=i, column=0, sticky="w", padx=12, pady=3)
            deger = ctk.CTkLabel(info, text="—", anchor="w", font=ctk.CTkFont(size=12))
            deger.grid(row=i, column=1, sticky="w", padx=(8, 12), pady=3)
            self.info_labels[anahtar] = deger
        info.columnconfigure(1, weight=1)

        # Harita
        if MAP_AVAILABLE:
            self.map_widget = TkinterMapView(self, width=420, height=300, corner_radius=0)
            self.map_widget.pack(fill="both", expand=True, padx=14, pady=6)
            self.map_widget.set_zoom(3)
        else:
            self.map_widget = None
            ctk.CTkLabel(self,
                         text="Harita için 'tkintermapview' kurulu değil.\n"
                              "Kurmak için:  pip install tkintermapview",
                         text_color=RENK_HATA, justify="center").pack(pady=10)

        # Yenile butonu
        self.btn = ctk.CTkButton(self, text="Yeniden Kontrol Et",
                                 command=self.check_ip)
        self.btn.pack(pady=(4, 14))

    # -------------------------------------------------------------- tema
    def _set_menu_value(self):
        mapping = {"Light": "Aydınlık", "Dark": "Karanlık", "System": "Sistem"}
        self.tema_menu.set(mapping.get(self.cfg.get("appearance", "System"), "Sistem"))

    def _change_theme(self, secim):
        mapping = {"Aydınlık": "Light", "Karanlık": "Dark", "Sistem": "System"}
        mode = mapping.get(secim, "System")
        ctk.set_appearance_mode(mode)
        self.cfg["appearance"] = mode
        save_config(self.cfg)
        self._apply_map_theme()

    def _apply_map_theme(self):
        """Temaya uygun harita tile'larını yükler."""
        if self.map_widget is None:
            return
        try:
            mode = ctk.get_appearance_mode()
        except Exception:
            mode = "Light"
        if mode == "Dark":
            self.map_widget.set_tile_server(TILE_DARK, max_zoom=19)
        else:
            self.map_widget.set_tile_server(TILE_LIGHT, max_zoom=19)

    # -------------------------------------------------------------- kontrol
    def check_ip(self):
        """Ağ isteğini arayüzü dondurmadan arka planda yapar."""
        self.btn.configure(state="disabled")
        self.status.configure(text="Kontrol ediliyor...", fg_color=RENK_BEKLE)
        t = threading.Thread(target=self._fetch, daemon=True)
        t.start()

    def _fetch(self):
        try:
            resp = requests.get(API_URL, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data.get("status") != "success":
                raise RuntimeError(data.get("message", "IP alınamadı"))
        except Exception as e:
            self.after(0, self._show_error, str(e))
            return
        self.after(0, self._update, data)

    # -------------------------------------------------------------- güncelle
    def _show_error(self, mesaj):
        self.status.configure(
            text="Bağlantı hatası: {}\nİnternet bağlantınızı kontrol edin.".format(mesaj),
            fg_color=RENK_HATA)
        self.btn.configure(state="normal")

    def _update(self, d):
        ip = d.get("query", "—")
        country = d.get("country", "—")
        code = d.get("countryCode", "")
        region = d.get("regionName", "")
        city = d.get("city", "")
        isp = d.get("isp", "—")
        lat = d.get("lat")
        lon = d.get("lon")

        self.info_labels["IP Adresi"].configure(text=ip)
        self.info_labels["Ülke"].configure(text="{} ({})".format(country, code))
        self.info_labels["Bölge / Şehir"].configure(text="{} / {}".format(region, city))
        self.info_labels["Sağlayıcı (ISP)"].configure(text=isp)
        self.info_labels["Koordinatlar"].configure(
            text="{}, {}".format(lat, lon) if lat is not None and lon is not None else "—")

        # VPN kontrolü: IP Türkiye'den mi?
        if code == TURKEY_CODE:
            self.status.configure(
                text="IP adresiniz TÜRKİYE'DEN geliyor.\n"
                     "VPN kapalı olabilir veya düzgün çalışmıyor.",
                fg_color=RENK_TURKIYE)
        else:
            self.status.configure(
                text="IP adresiniz TÜRKİYE DIŞINDAN geliyor ({}).\n"
                     "VPN çalışıyor gibi görünüyor.".format(country),
                fg_color=RENK_DISI)

        # Haritada göster
        if self.map_widget is not None and lat is not None and lon is not None:
            self.map_widget.set_position(lat, lon)
            self.map_widget.delete_all_marker()
            self.map_widget.set_marker(lat, lon, text=ip)
            self.map_widget.set_zoom(10 if city else 5)

        self.btn.configure(state="normal")


def main():
    app = VPNKontrolApp()
    app.mainloop()


if __name__ == "__main__":
    main()
