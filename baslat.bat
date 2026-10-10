@echo off
REM ============================================================
REM  VPN / Sansür Kontrol - Windows baslatici
REM  Ilk calistirmada gereken kutuphaneleri kurar ve uygulamayi acar.
REM ============================================================
cd /d "%~dp0"

echo Kutuphaneler kontrol ediliyor / kuruluyor...
python -m pip install -r requirements.txt

echo.
echo Uygulama baslatiliyor...
python vpn_kontrol.py

pause
