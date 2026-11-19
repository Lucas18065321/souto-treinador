@echo off
rem Abre o editor visual dos carrosséis no navegador (http://localhost:8765/editor). Feche esta janela para desligar.
chcp 65001 >nul
cd /d "%~dp0Gerador"
where python >nul 2>nul
if %errorlevel%==0 (
  python editor.py --abrir
) else (
  py -3 editor.py --abrir
)
pause
