# VPN / Sansür Kontrol

IP adresinizi gösteren, konumunuzu haritada gösteren ve IP'nin Türkiye'den
gelip gelmediğini kontrol ederek VPN'inizin çalışıp çalışmadığını anlatan
basit bir Windows programı.

## Ne yapar?
- IP adresinizi, ülke/şehir ve internet sağlayıcınızı gösterir.
- Konumunuzu harita üzerinde işaretler.
- IP Türkiye'den ise kırmızı, yurt dışından ise yeşil uyarı verir.
  - Kırmızı = VPN kapalı veya çalışmıyor olabilir.
  - Yeşil = VPN çalışıyor,İP adresiniz Türkiyede değil

## Nasıl çalıştırılır?

### 1. Hazır .exe ile (önerilen, Python gerekmez)
`VPN_Kontrol.exe` dosyasına çift tıklayın. Başka kurulum gerekmez.

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


