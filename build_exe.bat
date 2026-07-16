@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Close any old generator window first!
python -m pip install -r requirements.txt -q
python -m PyInstaller --noconfirm --clean --windowed --onefile ^
  --name "SillyTavernWorldbookMaker" ^
  --paths "." ^
  --hidden-import=customtkinter ^
  --collect-all customtkinter ^
  app.py
echo.
echo Done: dist\SillyTavernWorldbookMaker.exe
explorer dist
pause
