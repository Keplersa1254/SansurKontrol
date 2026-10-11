# VPN / Sansür Kontrol

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)](https://github.com/Keplersa1254/SansurKontrol)
[![Download](https://img.shields.io/badge/download-.exe-brightgreen.svg)](https://github.com/Keplersa1254/SansurKontrol/releases/latest)

IP adresinizi gösteren, konumunuzu haritada gösteren ve IP'nin Türkiye'den
gelip gelmediğini kontrol ederek VPN'inizin çalışıp çalışmadığını anlatan
basit bir Windows programı.

## Indirme linki

En son hazır programı buradan indirin:

**[VPN_Kontrol.exe indir](https://github.com/Keplersa1254/SansurKontrol/releases/latest/download/VPN_Kontrol.exe)**

Indirdikten sonra `VPN_Kontrol.exe` dosyasına çift tıklayın. Python kurmanıza
gerek yoktur.

> Tum surumler: https://github.com/Keplersa1254/SansurKontrol/releases

## Ne yapar?
- IP adresinizi, ülke/şehir ve internet sağlayıcınızı gösterir.
- Konumunuzu harita üzerinde işaretler.
- IP Türkiye'den ise kırmızı, yurt dışından ise yeşil uyarı verir.
  - Kırmızı = VPN kapalı veya çalışmıyor olabilir.
  - Yeşil = VPN çalışıyor,İP adresiniz Türkiyede değil
- Aydınlık / Karanlık / Sistem teması desteği (seçiminiz hatırlanır).

## Nasıl çalıştırılır?

### 1. Hazır .exe ile (önerilen, Python gerekmez)
Yukarıdaki **Indir** bölümünden `VPN_Kontrol.exe` dosyasını indirip çift
tıklayın. Başka kurulum gerekmez.

### 2. Kaynak koddan (Python ile)
1. Python'u kurun (python.org, "Add Python to PATH" işaretli olsun).
2. `baslat.bat` dosyasına çift tıklayın.

### 3. Kendi .exe dosyanızı yapmak için
1. Python kurulu olsun.
2. `build_exe.bat` dosyasına çift tıklayın.
3. Hazır program otomatik olarak Masaüstünüze kopyalanır:
   `Masaüstü\VPN_Kontrol.exe`

Bu .exe'yi istediğiniz herkese gönderebilirsiniz; onlarda Python kurulu
olmadan çalışır.

## Notlar
- İnternet bağlantısı gerekir (IP sorgusu ve harita için).
- IP sorgusu ücretsiz ip-api.com servisini kullanır.
- Harita OpenStreetMap üzerinden yüklenir.
- .exe oluşturma işlemi yalnızca Windows üzerinde yapılabilir.

YAŞASIN ÖZGÜR İNTERNET,KAHROLSUN SANSÜR!


