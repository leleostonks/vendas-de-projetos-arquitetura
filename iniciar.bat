@echo off
title RF Arquitetura - Dashboard
echo.
echo  ========================================
echo   RF Arquitetura - Dashboard de Vendas
echo  ========================================
echo.
cd /d "%~dp0"
python -m streamlit run app.py
pause
