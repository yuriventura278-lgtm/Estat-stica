"""
consulta.py — Funções CRUD para o serviço de Consulta Externa
Tabela principal: con_consultas
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── LISTAR ──────────────────────────────────────────────────────────────────

def listar_consultas(data=None, estado=None, especialidade=None):
    """
    Devolve a lista de consultas com filtros opcionais.
    - data: filtra pela data_consulta (formato YYYY-MM-DD)
    - estado: agendada, realizada, faltou, cancelada
    - especialidade: nome da especialidade
    """
    query = "SELECT * FROM con_consultas WHERE 1=1"
    params = []

    if data:
        query += " AND data_consulta = ?"
        params.append(data)

    if estado:
        query += " AND estado = ?"
        params.append(estado)

    if especialidade:
        query += " AND especialidade = ?"
        params.append(especialidade)

    query += " ORDER BY data_consulta DESC, hora ASC"

    with db.get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    return db.linhas_para_lista(rows)


# ─── CRIAR ───────────────────────────────────────────────────────────────────

def criar_consulta(dados):
    """
    Insere uma nova consulta na base de dados.
    ID gerado automaticamente com prefixo 'K'.
    Devolve o ID do novo registo.
    """
    novo_id = 'K' + str(uuid.uuid4())[:7].upper()

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO con_consultas
                (id, nome, nup, sexo, idade, especialidade, tipo, medico,
                 data_consulta, hora, motivo, estado)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :especialidade, :tipo, :medico,
                 :data_consulta, :hora, :motivo, :estado)
        """, {
            'id':           novo_id,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'especialidade': dados.get('especialidade', ''),
            'tipo':         dados.get('tipo', 'primeira'),
            'medico':       dados.get('medico', ''),
            'data_consulta': dados.get('data_consulta', ''),
            'hora':         dados.get('hora', ''),
            'motivo':       dados.get('motivo', ''),
            'estado':       dados.get('estado', 'agendada'),
        })

    return novo_id


# ─── ACTUALIZAR ──────────────────────────────────────────────────────────────

def actualizar_consulta(cid, dados):
    """
    Actualiza os campos clínicos de uma consulta existente.
    Campos actualizáveis: estado, diagnostico, prescricao, observacoes.
    """
    with db.get_conn() as conn:
        conn.execute("""
            UPDATE con_consultas
            SET estado      = :estado,
                diagnostico = :diagnostico,
                prescricao  = :prescricao,
                observacoes = :observacoes
            WHERE id = :id
        """, {
            'id':          cid,
            'estado':      dados.get('estado', 'agendada'),
            'diagnostico': dados.get('diagnostico', ''),
            'prescricao':  dados.get('prescricao', ''),
            'observacoes': dados.get('observacoes', ''),
        })


# ─── ELIMINAR ────────────────────────────────────────────────────────────────

def eliminar_consulta(cid):
    """Remove uma consulta pelo seu ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM con_consultas WHERE id = ?", (cid,))


# ─── ESTATÍSTICAS ────────────────────────────────────────────────────────────

def estatisticas_con(data_inicio, data_fim):
    """
    Calcula estatísticas das consultas num intervalo de datas.
    Devolve um dicionário com:
    - total: número total de consultas
    - realizadas, agendadas, faltou: contagens por estado
    - por_especialidade: dicionário {especialidade: contagem}
    """
    with db.get_conn() as conn:
        # Totais por estado
        rows_estado = conn.execute("""
            SELECT estado, COUNT(*) AS total
            FROM con_consultas
            WHERE data_consulta BETWEEN ? AND ?
            GROUP BY estado
        """, (data_inicio, data_fim)).fetchall()

        # Totais por especialidade
        rows_esp = conn.execute("""
            SELECT especialidade, COUNT(*) AS total
            FROM con_consultas
            WHERE data_consulta BETWEEN ? AND ?
            GROUP BY especialidade
            ORDER BY total DESC
        """, (data_inicio, data_fim)).fetchall()

    # Agregar contagens por estado
    contagens = {r['estado']: r['total'] for r in rows_estado}
    total = sum(contagens.values())

    # Dicionário de especialidades
    por_especialidade = {r['especialidade']: r['total'] for r in rows_esp}

    return {
        'total':          total,
        'realizadas':     contagens.get('realizada', 0),
        'agendadas':      contagens.get('agendada', 0),
        'faltou':         contagens.get('faltou', 0),
        'por_especialidade': por_especialidade,
    }
