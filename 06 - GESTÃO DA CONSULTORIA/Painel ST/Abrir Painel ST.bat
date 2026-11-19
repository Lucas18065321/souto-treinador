@echo off
rem Abre o Painel ST (o mesmo que o atalho da area de trabalho). Para a demonstracao com dados ficticios: Abrir Painel ST.bat --demo
cd /d "%~dp0"
start "" pythonw "%~dp0painel_st.py" --app %*
