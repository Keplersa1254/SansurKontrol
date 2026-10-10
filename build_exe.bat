@echo off
chcp 65001 >nul
REM ============================================================
REM  EXE OLUŞTURUCU (Windows)
REM  PyInstaller ile tek dosyalik VPN_Kontrol.exe uretir.
REM  Bitince otomatik olarak Masaustune kopyalar.
REM ============================================================
cd /d "%~dp0"

echo [1/3] PyInstaller kuruluyor / kontrol ediliyor...
python -m pip install --upgrade pyinstaller
if errorlevel 1 (
    echo PyInstaller kurulamadi! Python kurulu ve PATH'te oldugundan emin olun.
    pause
    exit /b 1
)

echo.
echo [2/3] Gereken kutuphaneler kuruluyor...
python -m pip install -r requirements.txt

echo.
echo [3/3] EXE olusturuluyor (bu biraz surebilir)...
python -m PyInstaller vpn_kontrol.spec --noconfirm --clean
if errorlevel 1 (
    echo EXE olusturulamadi.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo  BASARILI! EXE olustu.
echo ============================================================

REM Olusan exe'yi Masaustune kopyala
set "EXE_YOL=%cd%\dist\VPN_Kontrol.exe"
if exist "%EXE_YOL%" (
    copy /Y "%EXE_YOL%" "%USERPROFILE%\Desktop\VPN_Kontrol.exe" >nul
    if errorlevel 1 (
        echo Masaustune kopyalanamadi. Exe burada:
        echo     %EXE_YOL%
    ) else (
        echo Masaustunuze kopyalandi:
        echo     %USERPROFILE%\Desktop\VPN_Kontrol.exe
    )
) else (
    echo Exe bulunamadi: %EXE_YOL%
)

pause

