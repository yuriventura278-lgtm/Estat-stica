"""
auth.py — Autenticação de utilizadores
Funções de login, logout, hashing de senha e decorador login_required.
"""

import hashlib
import os
import sqlite3
from functools import wraps
from flask import session, redirect, url_for, request
import database as db


# ─── HASHING DE SENHA ────────────────────────────────────────────────────────

def _hash_senha(senha, sal=None):
    """
    Gera um hash seguro da senha usando SHA-256 + sal aleatório.
    Devolve a string "sal$hash".
    """
    if sal is None:
        sal = os.urandom(16).hex()          # 32 caracteres aleatórios
    h = hashlib.sha256((sal + senha).encode()).hexdigest()
    return f"{sal}${h}"


def verificar_senha(senha, hash_guardado):
    """Verifica se a senha corresponde ao hash guardado."""
    try:
        sal, _ = hash_guardado.split('$', 1)
        return _hash_senha(senha, sal) == hash_guardado
    except Exception:
        return False


# ─── OPERAÇÕES DE UTILIZADOR ─────────────────────────────────────────────────

def criar_utilizador(username, nome_completo, senha, cargo='enfermeiro', servico='geral'):
    """
    Cria um novo utilizador na base de dados.
    Lança ValueError se o username já existe.
    """
    if obter_utilizador_por_username(username):
        raise ValueError(f"Username '{username}' já existe")

    hash_senha = _hash_senha(senha)
    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO utilizadores (username, nome_completo, password_hash, cargo, servico)
            VALUES (?, ?, ?, ?, ?)
        """, (username.lower().strip(), nome_completo, hash_senha, cargo, servico))
    return True


def obter_utilizador_por_username(username):
    """Procura um utilizador pelo username. Devolve dict ou None."""
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM utilizadores WHERE username = ? AND activo = 1",
            (username.lower().strip(),)
        ).fetchone()
    return db.linha_para_dict(row)


def obter_utilizador_por_id(uid):
    """Procura um utilizador pelo ID."""
    with db.get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM utilizadores WHERE id = ?", (uid,)
        ).fetchone()
    return db.linha_para_dict(row)


def listar_utilizadores():
    """Lista todos os utilizadores activos."""
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT id, username, nome_completo, cargo, servico, criado FROM utilizadores ORDER BY nome_completo"
        ).fetchall()
    return db.linhas_para_lista(rows)


def alterar_senha(uid, senha_nova):
    """Altera a senha de um utilizador."""
    novo_hash = _hash_senha(senha_nova)
    with db.get_conn() as conn:
        conn.execute(
            "UPDATE utilizadores SET password_hash = ?, primeira_sessao = 0 WHERE id = ?",
            (novo_hash, uid)
        )


def desactivar_utilizador(uid):
    """Desactiva (não elimina) um utilizador."""
    with db.get_conn() as conn:
        conn.execute("UPDATE utilizadores SET activo = 0 WHERE id = ?", (uid,))


def autenticar(username, senha):
    """
    Verifica username + senha.
    Devolve o utilizador dict se correcto, None se errado.
    """
    u = obter_utilizador_por_username(username)
    if not u:
        return None
    if verificar_senha(senha, u['password_hash']):
        return u
    return None


# ─── DECORADOR login_required ─────────────────────────────────────────────────

def login_required(f):
    """
    Decorador que protege rotas: redireciona para /login se não autenticado.
    Uso:
        @app.route('/cirurgia')
        @login_required
        def pagina_cirurgia():
            ...
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('pagina_login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


def utilizador_actual():
    """Devolve o utilizador da sessão actual, ou None."""
    uid = session.get('user_id')
    if not uid:
        return None
    return obter_utilizador_por_id(uid)


# ─── CRIAR ADMIN PADRÃO ───────────────────────────────────────────────────────

def garantir_admin_padrao():
    """
    Cria o utilizador admin padrão se não existir nenhum utilizador.
    Credenciais iniciais: admin / admin123
    """
    with db.get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) as n FROM utilizadores").fetchone()['n']

    if total == 0:
        criar_utilizador(
            username='admin',
            nome_completo='Administrador do Sistema',
            senha='admin123',
            cargo='admin',
            servico='geral',
        )
        print("[AUTH] Utilizador admin criado. Senha inicial: admin123")
        print("[AUTH] ATENÇÃO: Altere a senha após o primeiro login!")
