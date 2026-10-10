"""
VPN / Sansür Kontrol
====================
IP adresinizi sorgular, konumunuzu haritada gösterir ve IP'nin
Türkiye'den gelip gelmediğini kontrol ederek VPN'in çalışıp
çalışmadığını anlamanızı sağlar.

Çalıştırma:
    python vpn_kontrol.py

Gereksinimler (kurulum):
    pip install -r requirements.txt
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk

import requests

# Harita kütüphanesi kurulu değilse program yine de çalışsın (harita hariç).
try:
    from tkintermapview import TkinterMapView
    MAP_AVAILABLE = True
except Exception:
    MAP_AVAILABLE = False

# Logo dosyasının yolu (hem script hem .exe içinde çalışsın).
if getattr(sys, "frozen", False):          # PyInstaller ile paketlendiğinde
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_PNG = os.path.join(BASE_DIR, "logo.png")
LOGO_ICO = os.path.join(BASE_DIR, "logo.ico")

# Ücretsiz, API anahtarı gerektirmeyen IP sorgulama servisi.
API_URL = "http://ip-api.com/json/"
TURKEY_CODE = "TR"

# Renkler
RENK_TURKIYE = "#c0392b"   # kırmızı
RENK_DISI = "#27ae60"      # yeşil
RENK_BEKLE = "#555555"     # gri


class VPNKontrolApp:
    def __init__(self, root):
        self.root = root
        root.title("VPN Kontrol – Sansür Kontrol")
        root.geometry("470x720")
        root.minsize(430, 680)

        # Pencere / görev çubuğu simgesi (.ico varsa)
        try:
            if os.path.exists(LOGO_ICO):
                root.iconbitmap(default=LOGO_ICO)
        except Exception:
            pass

        self._build_widgets()
        # Açılışta otomatik kontrol
        self.check_ip()

    # ------------------------------------------------------------------ UI
    def _build_widgets(self):
        # Başlık (logo + yazı)
        ust = tk.Frame(self.root)
        ust.pack(pady=(12, 4))
        try:
            from PIL import Image, ImageTk
            if os.path.exists(LOGO_PNG):
                img = Image.open(LOGO_PNG).convert("RGBA")
                img = img.resize((56, 56), Image.LANCZOS)
                self._logo = ImageTk.PhotoImage(img)  # referans tutulmali
                tk.Label(ust, image=self._logo).pack(side="left", padx=(0, 10))
        except Exception:
            pass
        tk.Label(ust, text="VPN / Sansür Kontrol",
                 font=("Segoe UI", 16, "bold")).pack(side="left")

        # Durum bandı (VPN çalışıyor mu?)
        self.status = tk.Label(self.root, text="Kontrol ediliyor...",
                               font=("Segoe UI", 12, "bold"),
                               fg="white", bg=RENK_BEKLE,
                               wraplength=400, justify="center",
                               padx=10, pady=10)
        self.status.pack(fill="x", padx=14, pady=6)

        # Bağlantı bilgileri
        info = tk.LabelFrame(self.root, text="Bağlantı Bilgileri", padx=10, pady=8)
        info.pack(fill="x", padx=14, pady=6)

        self.info_labels = {}
        satirlar = ["IP Adresi", "Ülke", "Bölge / Şehir", "Sağlayıcı (ISP)", "Koordinatlar"]
        for i, anahtar in enumerate(satirlar):
            tk.Label(info, text=anahtar + ":", anchor="w",
                     font=("Segoe UI", 10, "bold")).grid(
                row=i, column=0, sticky="w", pady=2)
            deger = tk.Label(info, text="—", anchor="w", font=("Segoe UI", 10))
            deger.grid(row=i, column=1, sticky="w", pady=2, padx=(8, 0))
            self.info_labels[anahtar] = deger
        info.columnconfigure(1, weight=1)

        # Harita
        if MAP_AVAILABLE:
            self.map_widget = TkinterMapView(self.root, width=420, height=290,
                                             corner_radius=0)
            self.map_widget.pack(fill="both", expand=True, padx=14, pady=6)
            self.map_widget.set_zoom(2)
        else:
            self.map_widget = None
            tk.Label(self.root,
                     text="Harita için 'tkintermapview' kurulu değil.\n"
                          "Kurmak için:  pip install tkintermapview",
                     fg="#aa0000", justify="center").pack(pady=10)

        # Yenile butonu
        self.btn = ttk.Button(self.root, text="Yeniden Kontrol Et",
                              command=self.check_ip)
        self.btn.pack(pady=(4, 14))

    # -------------------------------------------------------------- kontrol
    def check_ip(self):
        """Ağ isteğini arayüzü dondurmadan arka planda yapar."""
        self.btn.config(state="disabled")
        self.status.config(text="Kontrol ediliyor...", bg=RENK_BEKLE)
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
            # Hata mesajını ana iş parçacığında göster
            self.root.after(0, self._show_error, str(e))
            return
        self.root.after(0, self._update, data)

    # -------------------------------------------------------------- güncelle
    def _show_error(self, mesaj):
        self.status.config(
            text="Bağlantı hatası: {}\nİnternet bağlantınızı kontrol edin.".format(mesaj),
            bg="#aa0000")
        self.btn.config(state="normal")

    def _update(self, d):
        ip = d.get("query", "—")
        country = d.get("country", "—")
        code = d.get("countryCode", "")
        region = d.get("regionName", "")
        city = d.get("city", "")
        isp = d.get("isp", "—")
        lat = d.get("lat")
        lon = d.get("lon")

        self.info_labels["IP Adresi"].config(text=ip)
        self.info_labels["Ülke"].config(text="{} ({})".format(country, code))
        self.info_labels["Bölge / Şehir"].config(text="{} / {}".format(region, city))
        self.info_labels["Sağlayıcı (ISP)"].config(text=isp)
        self.info_labels["Koordinatlar"].config(
            text="{}, {}".format(lat, lon) if lat is not None and lon is not None else "—")

        # VPN kontrolü: IP Türkiye'den mi?
        if code == TURKEY_CODE:
            self.status.config(
                text="IP adresiniz TÜRKİYE'DEN geliyor.\n"
                     "VPN kapalı olabilir veya düzgün çalışmıyor.",
                bg=RENK_TURKIYE)
        else:
            self.status.config(
                text="IP adresiniz TÜRKİYE DIŞINDAN geliyor ({}).\n"
                     "VPN çalışıyor gibi görünüyor.".format(country),
                bg=RENK_DISI)

        # Haritada göster
        if self.map_widget is not None and lat is not None and lon is not None:
            self.map_widget.set_position(lat, lon)
            self.map_widget.delete_all_marker()
            self.map_widget.set_marker(lat, lon, text=ip)
            self.map_widget.set_zoom(8 if city else 4)

        self.btn.config(state="normal")


def main():
    root = tk.Tk()
    VPNKontrolApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()


