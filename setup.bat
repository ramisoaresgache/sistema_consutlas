@echo off
echo ==========================================
echo   SISTEMA DE CONSULTAS - INSTALACION
echo   Municipalidad de Vicente Lopez
echo ==========================================
echo.

echo [1/6] Verificando Python...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python no encontrado. Instalar Python 3.11 o superior.
    pause
    exit /b 1
)

echo.
echo [2/6] Creando entorno virtual...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudo crear el entorno virtual.
    pause
    exit /b 1
)

echo.
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate

echo.
echo [4/6] Actualizando pip...
python -m pip install --upgrade pip

echo.
echo [5/6] Instalando dependencias...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: No se pudieron instalar las dependencias.
    pause
    exit /b 1
)

echo.
echo [6/6] Configurando variables de entorno...
if not exist .env (
    copy .env.example .env
    echo.
    echo IMPORTANTE: Editar el archivo .env con las credenciales correctas!
    echo.
)

echo.
echo ==========================================
echo   INSTALACION COMPLETADA
echo ==========================================
echo.
echo Para ejecutar la aplicacion:
echo   1. Editar .env con las credenciales correctas
echo   2. Configurar usuarios_autorizados.py
echo   3. Ejecutar: streamlit run main.py
echo.
echo Presionar cualquier tecla para continuar...
pause >nul
