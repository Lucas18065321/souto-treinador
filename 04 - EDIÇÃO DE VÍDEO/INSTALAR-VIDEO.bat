@echo off
rem Instala o motor de video (SOUTO TREINADOR). Pode rodar de novo quantas vezes quiser.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0instalar-video.ps1" %*
