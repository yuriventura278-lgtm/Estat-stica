"""
database.py — Gestão da base de dados SQLite do Hospital do Prenda
Cria as tabelas e fornece funções de acesso aos dados.
"""

import sqlite3
import json
import os
from datetime import datetime

# Caminho para o ficheiro da base de dados
DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'hospital.db')


def get_conn():
    """Abre ligação à base de dados e activa chaves estrangeiras."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # permite aceder colunas por nome
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    """
    Cria todas as tabelas se ainda não existirem.
    Chamada uma vez ao iniciar o servidor.
    """
    with get_conn() as conn:
        conn.executescript("""

        -- ─── SERVIÇOS DO HOSPITAL ───────────────────────────────
        CREATE TABLE IF NOT EXISTS servicos (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo   TEXT NOT NULL UNIQUE,   -- ex: CIR, LAB, HIV
            nome     TEXT NOT NULL,           -- ex: Cirurgia Geral
            criado   TEXT DEFAULT (datetime('now'))
        );

        -- ─── HOSPITAIS / UNIDADES ───────────────────────────────
        CREATE TABLE IF NOT EXISTS hospitais (
            id     INTEGER PRIMARY KEY AUTOINCREMENT,
            nome   TEXT NOT NULL UNIQUE,
            criado TEXT DEFAULT (datetime('now'))
        );

        -- ─── DOENTES INTERNADOS (CIRURGIA GERAL) ────────────────
        CREATE TABLE IF NOT EXISTS cirurgia_doentes (
            id          TEXT PRIMARY KEY,          -- UUID gerado em Python
            nome        TEXT NOT NULL,
            sexo        TEXT CHECK(sexo IN ('M','F')),
            nup         TEXT,                      -- Número Único do Paciente
            idade       INTEGER,
            diagnostico TEXT,
            data_entrada TEXT NOT NULL,            -- formato: YYYY-MM-DD
            hospital    TEXT,
            internado   INTEGER DEFAULT 1,         -- 1=internado, 0=teve alta
            criado      TEXT DEFAULT (datetime('now')),
            actualizado TEXT DEFAULT (datetime('now'))
        );

        -- ─── ALTAS (CIRURGIA GERAL) ──────────────────────────────
        CREATE TABLE IF NOT EXISTS cirurgia_altas (
            id           TEXT PRIMARY KEY,
            doente_id    TEXT REFERENCES cirurgia_doentes(id),
            nome         TEXT NOT NULL,
            sexo         TEXT,
            nup          TEXT,
            idade        INTEGER,
            diagnostico  TEXT,                     -- diagnóstico à entrada
            diag_fim     TEXT,                     -- diagnóstico final
            data_entrada TEXT,
            data_saida   TEXT NOT NULL,
            modo_saida   TEXT,                     -- curado, melhorado, transferido, etc.
            hospital     TEXT,
            criado       TEXT DEFAULT (datetime('now'))
        );

        -- ─── ÓBITOS (CIRURGIA GERAL) ─────────────────────────────
        CREATE TABLE IF NOT EXISTS cirurgia_obitos (
            id           TEXT PRIMARY KEY,
            nome         TEXT NOT NULL,
            sexo         TEXT,
            nup          TEXT,
            idade        INTEGER,
            diagnostico  TEXT,
            diag_fim     TEXT,
            data_entrada TEXT,
            data_obito   TEXT NOT NULL,
            hospital     TEXT,
            criado       TEXT DEFAULT (datetime('now'))
        );

        -- ─── LOTAÇÃO DE CAMAS (CIRURGIA GERAL) ───────────────────
        CREATE TABLE IF NOT EXISTS cirurgia_camas (
            data    TEXT PRIMARY KEY,              -- formato: YYYY-MM-DD
            camas   INTEGER NOT NULL DEFAULT 0,
            criado  TEXT DEFAULT (datetime('now'))
        );

        -- ─── ÍNDICES para pesquisa rápida ────────────────────────
        CREATE INDEX IF NOT EXISTS idx_cir_doentes_data
            ON cirurgia_doentes(data_entrada);

        CREATE INDEX IF NOT EXISTS idx_cir_altas_data
            ON cirurgia_altas(data_saida);

        CREATE INDEX IF NOT EXISTS idx_cir_obitos_data
            ON cirurgia_obitos(data_obito);

        -- ─── DADOS INICIAIS ───────────────────────────────────────
        INSERT OR IGNORE INTO servicos (codigo, nome) VALUES
            ('CIR', 'Cirurgia Geral'),
            ('LAB', 'Laboratório'),
            ('HIV', 'VIH / SIDA'),
            ('HEM', 'Hemoterapia'),
            ('IMG', 'Imagiologia'),
            ('CON', 'Consulta Externa'),
            ('BLO', 'Bloco Operatório'),
            ('FIS', 'Fisioterapia');

        INSERT OR IGNORE INTO hospitais (nome) VALUES
            ('Hospital do Prenda'),
            ('Hospital Américo Boavida'),
            ('Hospital Josina Machel'),
            ('Hospital Militar'),
            ('Clínica Sagrada Esperança');

        """)
    print(f"[DB] Base de dados pronta: {DB_PATH}")


# ─── FUNÇÕES AUXILIARES ──────────────────────────────────────────────────────

def linha_para_dict(row):
    """Converte uma linha SQLite num dicionário Python."""
    return dict(row) if row else None


def linhas_para_lista(rows):
    """Converte múltiplas linhas SQLite numa lista de dicionários."""
    return [dict(r) for r in rows]


# ─── HOSPITAIS ───────────────────────────────────────────────────────────────

def listar_hospitais():
    """Devolve a lista de hospitais registados."""
    with get_conn() as conn:
        rows = conn.execute("SELECT nome FROM hospitais ORDER BY nome").fetchall()
    return [r['nome'] for r in rows]


# ─── CIRURGIA — DOENTES ──────────────────────────────────────────────────────

def listar_doentes_internados(data=None):
    """
    Devolve todos os doentes actualmente internados.
    Se 'data' for fornecida, filtra doentes que estavam internados nessa data.
    """
    with get_conn() as conn:
        if data:
            rows = conn.execute("""
                SELECT * FROM cirurgia_doentes
                WHERE data_entrada <= ?
                  AND (internado = 1 OR id IN (
                      SELECT doente_id FROM cirurgia_altas WHERE data_saida >= ?
                  ))
                ORDER BY data_entrada DESC
            """, (data, data)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM cirurgia_doentes
                WHERE internado = 1
                ORDER BY data_entrada DESC
            """).fetchall()
    return linhas_para_lista(rows)


def obter_doente(doente_id):
    """Devolve um doente pelo seu ID."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM cirurgia_doentes WHERE id = ?", (doente_id,)
        ).fetchone()
    return linha_para_dict(row)


def criar_doente(dados):
    """
    Insere um novo doente na base de dados.
    'dados' é um dicionário com os campos do doente.
    Devolve o ID do novo registo.
    """
    import uuid
    novo_id = str(uuid.uuid4())[:8].upper()   # ID curto: ex. A3F7B2C1
    agora = datetime.now().isoformat(timespec='seconds')

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO cirurgia_doentes
                (id, nome, sexo, nup, idade, diagnostico, data_entrada, hospital, internado, criado, actualizado)
            VALUES
                (:id, :nome, :sexo, :nup, :idade, :diagnostico, :data_entrada, :hospital, 1, :agora, :agora)
        """, {
            'id':          novo_id,
            'nome':        dados.get('nome', ''),
            'sexo':        dados.get('sexo', ''),
            'nup':         dados.get('nup', ''),
            'idade':       dados.get('idade'),
            'diagnostico': dados.get('diagnostico', ''),
            'data_entrada': dados.get('data_entrada', datetime.today().strftime('%Y-%m-%d')),
            'hospital':    dados.get('hospital', 'Hospital do Prenda'),
            'agora':       agora,
        })
    return novo_id


def actualizar_doente(doente_id, dados):
    """Actualiza os dados de um doente existente."""
    agora = datetime.now().isoformat(timespec='seconds')
    with get_conn() as conn:
        conn.execute("""
            UPDATE cirurgia_doentes
            SET nome=:nome, sexo=:sexo, nup=:nup, idade=:idade,
                diagnostico=:diagnostico, data_entrada=:data_entrada,
                hospital=:hospital, actualizado=:agora
            WHERE id=:id
        """, {
            'id':          doente_id,
            'nome':        dados.get('nome', ''),
            'sexo':        dados.get('sexo', ''),
            'nup':         dados.get('nup', ''),
            'idade':       dados.get('idade'),
            'diagnostico': dados.get('diagnostico', ''),
            'data_entrada': dados.get('data_entrada', ''),
            'hospital':    dados.get('hospital', ''),
            'agora':       agora,
        })


def eliminar_doente(doente_id):
    """Remove um doente pelo ID."""
    with get_conn() as conn:
        conn.execute("DELETE FROM cirurgia_doentes WHERE id = ?", (doente_id,))


# ─── CIRURGIA — ALTAS ────────────────────────────────────────────────────────

def listar_altas(data_inicio=None, data_fim=None):
    """Devolve as altas, com filtro opcional por período."""
    with get_conn() as conn:
        if data_inicio and data_fim:
            rows = conn.execute("""
                SELECT * FROM cirurgia_altas
                WHERE data_saida BETWEEN ? AND ?
                ORDER BY data_saida DESC
            """, (data_inicio, data_fim)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM cirurgia_altas ORDER BY data_saida DESC"
            ).fetchall()
    return linhas_para_lista(rows)


def registar_alta(doente_id, dados):
    """
    Regista a alta de um doente:
    1. Insere na tabela cirurgia_altas
    2. Marca o doente como internado=0 em cirurgia_doentes
    """
    import uuid
    novo_id = 'A' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    doente = obter_doente(doente_id)
    if not doente:
        raise ValueError(f"Doente {doente_id} não encontrado")

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO cirurgia_altas
                (id, doente_id, nome, sexo, nup, idade, diagnostico, diag_fim,
                 data_entrada, data_saida, modo_saida, hospital, criado)
            VALUES
                (:id, :doente_id, :nome, :sexo, :nup, :idade, :diagnostico, :diag_fim,
                 :data_entrada, :data_saida, :modo_saida, :hospital, :agora)
        """, {
            'id':          novo_id,
            'doente_id':   doente_id,
            'nome':        doente['nome'],
            'sexo':        doente['sexo'],
            'nup':         doente['nup'],
            'idade':       doente['idade'],
            'diagnostico': doente['diagnostico'],
            'diag_fim':    dados.get('diag_fim', ''),
            'data_entrada': doente['data_entrada'],
            'data_saida':  dados.get('data_saida', datetime.today().strftime('%Y-%m-%d')),
            'modo_saida':  dados.get('modo_saida', ''),
            'hospital':    doente['hospital'],
            'agora':       agora,
        })
        # marcar doente como sem internamento
        conn.execute(
            "UPDATE cirurgia_doentes SET internado=0, actualizado=? WHERE id=?",
            (agora, doente_id)
        )
    return novo_id


def eliminar_alta(alta_id):
    """Remove um registo de alta."""
    with get_conn() as conn:
        conn.execute("DELETE FROM cirurgia_altas WHERE id = ?", (alta_id,))


# ─── CIRURGIA — ÓBITOS ───────────────────────────────────────────────────────

def listar_obitos(data_inicio=None, data_fim=None):
    """Devolve os óbitos, com filtro opcional por período."""
    with get_conn() as conn:
        if data_inicio and data_fim:
            rows = conn.execute("""
                SELECT * FROM cirurgia_obitos
                WHERE data_obito BETWEEN ? AND ?
                ORDER BY data_obito DESC
            """, (data_inicio, data_fim)).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM cirurgia_obitos ORDER BY data_obito DESC"
            ).fetchall()
    return linhas_para_lista(rows)


def registar_obito(dados):
    """Regista um óbito directamente (sem exigir doente_id)."""
    import uuid
    novo_id = 'O' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    with get_conn() as conn:
        conn.execute("""
            INSERT INTO cirurgia_obitos
                (id, nome, sexo, nup, idade, diagnostico, diag_fim,
                 data_entrada, data_obito, hospital, criado)
            VALUES
                (:id, :nome, :sexo, :nup, :idade, :diagnostico, :diag_fim,
                 :data_entrada, :data_obito, :hospital, :agora)
        """, {
            'id':          novo_id,
            'nome':        dados.get('nome', ''),
            'sexo':        dados.get('sexo', ''),
            'nup':         dados.get('nup', ''),
            'idade':       dados.get('idade'),
            'diagnostico': dados.get('diagnostico', ''),
            'diag_fim':    dados.get('diag_fim', ''),
            'data_entrada': dados.get('data_entrada', ''),
            'data_obito':  dados.get('data_obito', datetime.today().strftime('%Y-%m-%d')),
            'hospital':    dados.get('hospital', 'Hospital do Prenda'),
            'agora':       agora,
        })
    return novo_id


def eliminar_obito(obito_id):
    """Remove um registo de óbito."""
    with get_conn() as conn:
        conn.execute("DELETE FROM cirurgia_obitos WHERE id = ?", (obito_id,))


# ─── CIRURGIA — CAMAS ────────────────────────────────────────────────────────

def obter_camas(data):
    """Devolve o número de camas registado para uma data específica."""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT camas FROM cirurgia_camas WHERE data = ?", (data,)
        ).fetchone()
    return row['camas'] if row else 0


def guardar_camas(data, quantidade):
    """Guarda ou actualiza o número de camas para uma data."""
    with get_conn() as conn:
        conn.execute("""
            INSERT INTO cirurgia_camas (data, camas)
            VALUES (?, ?)
            ON CONFLICT(data) DO UPDATE SET camas=excluded.camas
        """, (data, quantidade))


# ─── EXPORTAR / IMPORTAR JSON ────────────────────────────────────────────────

def exportar_json(servico='cirurgia'):
    """
    Exporta todos os dados de um serviço para um dicionário Python.
    Pode ser guardado como ficheiro .json.
    """
    with get_conn() as conn:
        doentes = linhas_para_lista(conn.execute("SELECT * FROM cirurgia_doentes").fetchall())
        altas   = linhas_para_lista(conn.execute("SELECT * FROM cirurgia_altas").fetchall())
        obitos  = linhas_para_lista(conn.execute("SELECT * FROM cirurgia_obitos").fetchall())
        camas   = linhas_para_lista(conn.execute("SELECT * FROM cirurgia_camas").fetchall())

    return {
        'servico':   servico,
        'exportado': datetime.now().isoformat(timespec='seconds'),
        'doentes':   doentes,
        'altas':     altas,
        'obitos':    obitos,
        'camas':     camas,
    }


def importar_json(dados_json):
    """
    Importa dados de um dicionário JSON para a base de dados.
    Usa INSERT OR IGNORE para não duplicar registos existentes.
    """
    agora = datetime.now().isoformat(timespec='seconds')
    with get_conn() as conn:
        for d in dados_json.get('doentes', []):
            conn.execute("""
                INSERT OR IGNORE INTO cirurgia_doentes
                    (id, nome, sexo, nup, idade, diagnostico, data_entrada, hospital, internado, criado, actualizado)
                VALUES
                    (:id, :nome, :sexo, :nup, :idade, :diagnostico, :data_entrada, :hospital, :internado, :criado, :actualizado)
            """, {**d, 'criado': d.get('criado', agora), 'actualizado': d.get('actualizado', agora)})

        for a in dados_json.get('altas', []):
            conn.execute("""
                INSERT OR IGNORE INTO cirurgia_altas
                    (id, doente_id, nome, sexo, nup, idade, diagnostico, diag_fim,
                     data_entrada, data_saida, modo_saida, hospital, criado)
                VALUES
                    (:id, :doente_id, :nome, :sexo, :nup, :idade, :diagnostico, :diag_fim,
                     :data_entrada, :data_saida, :modo_saida, :hospital, :criado)
            """, {**a, 'criado': a.get('criado', agora)})

        for o in dados_json.get('obitos', []):
            conn.execute("""
                INSERT OR IGNORE INTO cirurgia_obitos
                    (id, nome, sexo, nup, idade, diagnostico, diag_fim,
                     data_entrada, data_obito, hospital, criado)
                VALUES
                    (:id, :nome, :sexo, :nup, :idade, :diagnostico, :diag_fim,
                     :data_entrada, :data_obito, :hospital, :criado)
            """, {**o, 'criado': o.get('criado', agora)})

        for c in dados_json.get('camas', []):
            conn.execute("""
                INSERT OR IGNORE INTO cirurgia_camas (data, camas) VALUES (:data, :camas)
            """, c)

    return True
