@echo off
chcp 65001 >nul
title Hospital do Prenda — Instalação

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   Hospital do Prenda — Instalação            ║
echo  ║   Sistema de Gestão Hospitalar               ║
echo  ╚══════════════════════════════════════════════╝
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERRO] Python não encontrado!
    echo.
    echo  Por favor instala o Python primeiro:
    echo  1. Vai a: https://www.python.org/downloads/
    echo  2. Descarrega a versão mais recente
    echo  3. Durante a instalação, marca "Add Python to PATH"
    echo  4. Depois corre este ficheiro novamente
    echo.
    pause
    exit /b 1
)

echo  [OK] Python encontrado.
echo.
echo  A instalar dependências...
echo.

pip install flask --quiet
if errorlevel 1 (
    echo  [ERRO] Falha ao instalar Flask.
    echo  Verifica a tua ligação à internet e tenta novamente.
    pause
    exit /b 1
)

echo  [OK] Flask instalado com sucesso.
echo.

:: Criar pasta de dados se não existir
if not exist "data" mkdir data
if not exist "exports" mkdir exports

echo  ╔══════════════════════════════════════════════╗
echo  ║   Instalação concluída com sucesso!          ║
echo  ║                                              ║
echo  ║   Para iniciar o sistema:                    ║
echo  ║   → Duplo clique em  INICIAR.bat             ║
echo  ╚══════════════════════════════════════════════╝
echo.
pause
