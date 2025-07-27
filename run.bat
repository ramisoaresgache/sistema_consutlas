@echo off
title Sistema de Consultas - Municipalidad de Vicente Lopez

echo ==========================================
echo   SISTEMA DE CONSULTAS
echo   Municipalidad de Vicente Lopez
echo ==========================================
echo.

echo Activando entorno virtual...
call venv\Scripts\activate

echo.
echo Iniciando aplicacion...
echo.
echo La aplicacion se abrira en: http://localhost:8501
echo.
echo Para detener la aplicacion: Ctrl+C
echo.

streamlit run main.py

pause
