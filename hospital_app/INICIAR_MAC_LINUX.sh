#!/bin/bash
# Hospital do Prenda — Iniciar sistema (Mac / Linux)

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   Hospital do Prenda — Sistema de Gestão     ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python 3 não encontrado."
    echo "Instala com:  sudo apt install python3 python3-pip  (Linux)"
    echo "          ou  brew install python  (Mac)"
    exit 1
fi

# Instalar Flask se necessário
python3 -c "import flask" 2>/dev/null || {
    echo "A instalar Flask..."
    pip3 install flask
}

# Criar pastas
mkdir -p data exports

echo "[OK] A iniciar servidor..."
echo ""
echo "┌─────────────────────────────────────────────┐"
echo "│  Endereço:   http://localhost:5000           │"
echo "│  Utilizador: admin                           │"
echo "│  Senha:      admin123                        │"
echo "│  Para parar: Ctrl+C                          │"
echo "└─────────────────────────────────────────────┘"
echo ""

# Abrir browser (Mac e Linux)
sleep 2 && (open http://localhost:5000 2>/dev/null || xdg-open http://localhost:5000 2>/dev/null) &

python3 app.py
