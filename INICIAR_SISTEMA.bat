@echo off
TITLE GHOST STATION - INICIALIZANDO...
color 0A

echo ==========================================
echo      INICIANDO GHOST STATION V2.0
echo ==========================================
echo.
echo 1. Ativando Ambiente Virtual...
cd /d "C:\Users\Mauricio\Desktop\ghost_station"
call venv\Scripts\activate

echo.
echo 2. Verificando Dependencias...
pip install -q -r requirements.txt

echo.
echo 3. Iniciando Servidor Neural...
echo    Acesse: http://127.0.0.1:8000
echo.
python manage.py runserver

pause