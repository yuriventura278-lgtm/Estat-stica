"""
fisioterapia.py — Funções CRUD para o serviço de Fisioterapia
Tabelas: fisio_doentes, fisio_sessoes
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── DOENTES — LISTAR ────────────────────────────────────────────────────────

def listar_doentes(activo=True):
    """
    Devolve a lista de doentes de fisioterapia.
    - activo=True: apenas doentes activos (em tratamento)
    - activo=False: apenas doentes inactivos (alta/saída)
    """
    with db.get_conn() as conn:
        rows = conn.execute("""
            SELECT * FROM fisio_doentes
            WHERE activo = ?
            ORDER BY nome ASC
        """, (1 if activo else 0,)).fetchall()

    return db.linhas_para_lista(rows)


# ─── DOENTES — CRIAR ─────────────────────────────────────────────────────────

def criar_doente(dados):
    """
    Insere um novo doente na tabela fisio_doentes.
    ID gerado automaticamente com prefixo 'F'.
    Devolve o ID do novo registo.
    """
    novo_id = 'F' + str(uuid.uuid4())[:7].upper()

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO fisio_doentes
                (id, nome, nup, sexo, idade, diagnostico, patologia,
                 medico_ref, data_entrada, activo)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :diagnostico, :patologia,
                 :medico_ref, :data_entrada, 1)
        """, {
            'id':           novo_id,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'diagnostico':  dados.get('diagnostico', ''),
            'patologia':    dados.get('patologia', ''),
            'medico_ref':   dados.get('medico_ref', ''),
            'data_entrada': dados.get('data_entrada', ''),
        })

    return novo_id


# ─── DOENTES — ACTUALIZAR ────────────────────────────────────────────────────

def actualizar_doente(fid, dados):
    """Actualiza os dados de um doente de fisioterapia."""
    with db.get_conn() as conn:
        conn.execute("""
            UPDATE fisio_doentes
            SET nome        = :nome,
                nup         = :nup,
                sexo        = :sexo,
                idade       = :idade,
                diagnostico = :diagnostico,
                patologia   = :patologia,
                medico_ref  = :medico_ref,
                data_entrada = :data_entrada
            WHERE id = :id
        """, {
            'id':           fid,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'diagnostico':  dados.get('diagnostico', ''),
            'patologia':    dados.get('patologia', ''),
            'medico_ref':   dados.get('medico_ref', ''),
            'data_entrada': dados.get('data_entrada', ''),
        })


# ─── DOENTES — DESACTIVAR ────────────────────────────────────────────────────

def desactivar_doente(fid):
    """Marca o doente como inactivo (alta ou saída do serviço)."""
    with db.get_conn() as conn:
        conn.execute(
            "UPDATE fisio_doentes SET activo = 0 WHERE id = ?", (fid,)
        )


# ─── SESSÕES — LISTAR ────────────────────────────────────────────────────────

def listar_sessoes(doente_id=None, data_inicio=None, data_fim=None):
    """
    Devolve a lista de sessões de fisioterapia com filtros opcionais.
    - doente_id: filtra sessões de um doente específico
    - data_inicio / data_fim: filtra por intervalo de datas
    """
    query = "SELECT * FROM fisio_sessoes WHERE 1=1"
    params = []

    if doente_id:
        query += " AND doente_id = ?"
        params.append(doente_id)

    if data_inicio and data_fim:
        query += " AND data_sessao BETWEEN ? AND ?"
        params.extend([data_inicio, data_fim])
    elif data_inicio:
        query += " AND data_sessao >= ?"
        params.append(data_inicio)
    elif data_fim:
        query += " AND data_sessao <= ?"
        params.append(data_fim)

    query += " ORDER BY data_sessao DESC, num_sessao DESC"

    with db.get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    return db.linhas_para_lista(rows)


# ─── SESSÕES — REGISTAR ──────────────────────────────────────────────────────

def registar_sessao(dados):
    """
    Insere uma nova sessão de fisioterapia.
    ID gerado automaticamente com prefixo 'S'.
    O num_sessao é calculado automaticamente (sessões anteriores do doente + 1).
    Devolve o ID do novo registo.
    """
    novo_id = 'S' + str(uuid.uuid4())[:7].upper()
    doente_id = dados.get('doente_id', '')

    with db.get_conn() as conn:
        # Calcular número sequencial da sessão para este doente
        row = conn.execute("""
            SELECT COUNT(*) AS total FROM fisio_sessoes WHERE doente_id = ?
        """, (doente_id,)).fetchone()
        num_sessao = (row['total'] if row else 0) + 1

        conn.execute("""
            INSERT INTO fisio_sessoes
                (id, doente_id, nome_doente, data_sessao, num_sessao,
                 tipo_terapia, fisioterapeuta, duracao_min, evolucao, observacoes)
            VALUES
                (:id, :doente_id, :nome_doente, :data_sessao, :num_sessao,
                 :tipo_terapia, :fisioterapeuta, :duracao_min, :evolucao, :observacoes)
        """, {
            'id':             novo_id,
            'doente_id':      doente_id,
            'nome_doente':    dados.get('nome_doente', ''),
            'data_sessao':    dados.get('data_sessao', ''),
            'num_sessao':     num_sessao,
            'tipo_terapia':   dados.get('tipo_terapia', ''),
            'fisioterapeuta': dados.get('fisioterapeuta', ''),
            'duracao_min':    dados.get('duracao_min', 30),
            'evolucao':       dados.get('evolucao', ''),
            'observacoes':    dados.get('observacoes', ''),
        })

    return novo_id


# ─── SESSÕES — ELIMINAR ──────────────────────────────────────────────────────

def eliminar_sessao(sid):
    """Remove uma sessão pelo seu ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM fisio_sessoes WHERE id = ?", (sid,))


# ─── ESTATÍSTICAS ────────────────────────────────────────────────────────────

def estatisticas_fisio(data_inicio, data_fim):
    """
    Calcula estatísticas do serviço de fisioterapia num intervalo de datas.
    Devolve um dicionário com:
    - total_doentes: doentes com pelo menos uma sessão no período
    - total_sessoes: total de sessões realizadas no período
    - media_sessoes_por_doente: média de sessões por doente
    - por_evolucao: dicionário {melhora, sem_alteracao, piora} com contagens
    """
    with db.get_conn() as conn:
        # Total de sessões e doentes distintos no período
        row_totais = conn.execute("""
            SELECT
                COUNT(*)                    AS total_sessoes,
                COUNT(DISTINCT doente_id)   AS total_doentes
            FROM fisio_sessoes
            WHERE data_sessao BETWEEN ? AND ?
        """, (data_inicio, data_fim)).fetchone()

        # Contagens por evolução
        rows_evolucao = conn.execute("""
            SELECT evolucao, COUNT(*) AS total
            FROM fisio_sessoes
            WHERE data_sessao BETWEEN ? AND ?
            GROUP BY evolucao
        """, (data_inicio, data_fim)).fetchall()

    total_sessoes = row_totais['total_sessoes'] if row_totais else 0
    total_doentes = row_totais['total_doentes'] if row_totais else 0

    # Calcular média de sessões por doente
    media = round(total_sessoes / total_doentes, 2) if total_doentes > 0 else 0

    # Agregar evolução
    por_evolucao_raw = {r['evolucao']: r['total'] for r in rows_evolucao}

    return {
        'total_doentes':           total_doentes,
        'total_sessoes':           total_sessoes,
        'media_sessoes_por_doente': media,
        'por_evolucao': {
            'melhora':        por_evolucao_raw.get('melhora', 0),
            'sem_alteracao':  por_evolucao_raw.get('sem_alteracao', 0),
            'piora':          por_evolucao_raw.get('piora', 0),
        },
    }
