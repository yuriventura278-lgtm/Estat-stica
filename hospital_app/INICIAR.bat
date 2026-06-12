@echo off
chcp 65001 >nul
title Hospital do Prenda — Sistema em execução

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   Hospital do Prenda — Sistema de Gestão     ║
echo  ║   A iniciar servidor...                      ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python não encontrado. Corre primeiro o INSTALAR.bat
    pause
    exit /b 1
)

:: Verificar Flask
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo  [AVISO] Flask não instalado. A instalar agora...
    pip install flask --quiet
)

:: Criar pastas necessárias
if not exist "data" mkdir data
if not exist "exports" mkdir exports

echo  [OK] A abrir o browser em 3 segundos...
echo.
echo  ┌─────────────────────────────────────────────┐
echo  │  Endereço:   http://localhost:5000           │
echo  │  Utilizador: admin                           │
echo  │  Senha:      admin123                        │
echo  │                                              │
echo  │  Para parar o servidor: fechar esta janela  │
echo  └─────────────────────────────────────────────┘
echo.

:: Abrir browser após 3 segundos
start /b cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

:: Iniciar servidor Flask
python app.py

echo.
echo  Servidor parado.
pause
