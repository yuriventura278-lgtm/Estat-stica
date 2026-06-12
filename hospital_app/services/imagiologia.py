"""
imagiologia.py — Funções CRUD para o serviço de Imagiologia
Tabela principal: imag_exames
"""

import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── EXAMES ───────────────────────────────────────────────────────────────────

def listar_exames(data_inicio=None, data_fim=None, estado=None, tipo_exame=None):
    """
    Devolve a lista de exames de imagiologia.
    Filtros opcionais: intervalo de datas, estado e tipo de exame.
    """
    sql = "SELECT * FROM imag_exames WHERE 1=1"
    params = []

    if data_inicio and data_fim:
        sql += " AND data_req BETWEEN ? AND ?"
        params += [data_inicio, data_fim]
    elif data_inicio:
        sql += " AND data_req >= ?"
        params.append(data_inicio)
    elif data_fim:
        sql += " AND data_req <= ?"
        params.append(data_fim)

    if estado:
        sql += " AND estado = ?"
        params.append(estado)

    if tipo_exame:
        sql += " AND tipo_exame = ?"
        params.append(tipo_exame)

    sql += " ORDER BY data_req DESC"

    with db.get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return db.linhas_para_lista(rows)


def criar_exame(dados):
    """
    Cria um novo pedido de exame de imagiologia.
    Gera ID com prefixo 'I'. Devolve o ID criado.
    """
    novo_id = 'I' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO imag_exames
                (id, nome, nup, sexo, idade, tipo_exame, regiao,
                 urgente, medico_req, data_req, estado, criado)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :tipo_exame, :regiao,
                 :urgente, :medico_req, :data_req, 'pendente', :agora)
        """, {
            'id':         novo_id,
            'nome':       dados.get('nome', ''),
            'nup':        dados.get('nup', ''),
            'sexo':       dados.get('sexo', ''),
            'idade':      dados.get('idade'),
            'tipo_exame': dados.get('tipo_exame', ''),
            'regiao':     dados.get('regiao', ''),
            'urgente':    int(dados.get('urgente', 0)),
            'medico_req': dados.get('medico_req', ''),
            'data_req':   dados.get('data_req', datetime.today().strftime('%Y-%m-%d')),
            'agora':      agora,
        })
    return novo_id


def actualizar_resultado(exame_id, resultado, conclusao, data_result=None):
    """
    Regista o resultado e conclusão de um exame e marca o estado como 'concluido'.
    Se data_result não for fornecida, usa a data de hoje.
    """
    if not data_result:
        data_result = datetime.today().strftime('%Y-%m-%d')

    with db.get_conn() as conn:
        conn.execute("""
            UPDATE imag_exames
            SET resultado = ?, conclusao = ?, data_result = ?, estado = 'concluido'
            WHERE id = ?
        """, (resultado, conclusao, data_result, exame_id))


def eliminar_exame(eid):
    """Remove um exame de imagiologia pelo ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM imag_exames WHERE id = ?", (eid,))


# ─── ESTATÍSTICAS ─────────────────────────────────────────────────────────────

def estatisticas_imag(inicio, fim):
    """
    Devolve estatísticas do serviço de imagiologia para o período indicado.
    Retorna: total, pendentes, concluidos, por_tipo (contagem por tipo de exame).
    """
    with db.get_conn() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM imag_exames WHERE data_req BETWEEN ? AND ?",
            (inicio, fim)
        ).fetchone()[0]

        pendentes = conn.execute(
            "SELECT COUNT(*) FROM imag_exames WHERE data_req BETWEEN ? AND ? AND estado = 'pendente'",
            (inicio, fim)
        ).fetchone()[0]

        concluidos = conn.execute(
            "SELECT COUNT(*) FROM imag_exames WHERE data_req BETWEEN ? AND ? AND estado = 'concluido'",
            (inicio, fim)
        ).fetchone()[0]

        # Contagem por tipo de exame no período
        rows_tipo = conn.execute("""
            SELECT tipo_exame, COUNT(*) as total
            FROM imag_exames
            WHERE data_req BETWEEN ? AND ?
            GROUP BY tipo_exame
            ORDER BY total DESC
        """, (inicio, fim)).fetchall()
        por_tipo = {r['tipo_exame']: r['total'] for r in rows_tipo}

    return {
        'total':      total,
        'pendentes':  pendentes,
        'concluidos': concluidos,
        'por_tipo':   por_tipo,
    }
