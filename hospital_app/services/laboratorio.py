"""
laboratorio.py — Funções CRUD para o serviço de Laboratório
Tabela principal: lab_requisicoes
"""

import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── REQUISIÇÕES ─────────────────────────────────────────────────────────────

def listar_requisicoes(data_inicio=None, data_fim=None, estado=None):
    """
    Devolve a lista de requisições do laboratório.
    Filtros opcionais: intervalo de datas e/ou estado (pendente, em_curso, concluido).
    """
    sql = "SELECT * FROM lab_requisicoes WHERE 1=1"
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

    sql += " ORDER BY data_req DESC"

    with db.get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return db.linhas_para_lista(rows)


def criar_requisicao(dados):
    """
    Cria uma nova requisição de análise laboratorial.
    Gera um ID único com prefixo 'L'.
    Devolve o ID criado.
    """
    novo_id = 'L' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO lab_requisicoes
                (id, nome, nup, sexo, idade, tipo_analise, urgente,
                 medico_req, data_req, estado, criado)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :tipo_analise, :urgente,
                 :medico_req, :data_req, 'pendente', :agora)
        """, {
            'id':           novo_id,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'tipo_analise': dados.get('tipo_analise', ''),
            'urgente':      int(dados.get('urgente', 0)),
            'medico_req':   dados.get('medico_req', ''),
            'data_req':     dados.get('data_req', datetime.today().strftime('%Y-%m-%d')),
            'agora':        agora,
        })
    return novo_id


def actualizar_resultado(req_id, resultado, data_result=None):
    """
    Regista o resultado de uma análise e marca o estado como 'concluido'.
    Se data_result não for fornecida, usa a data de hoje.
    """
    if not data_result:
        data_result = datetime.today().strftime('%Y-%m-%d')

    with db.get_conn() as conn:
        conn.execute("""
            UPDATE lab_requisicoes
            SET resultado = ?, data_result = ?, estado = 'concluido'
            WHERE id = ?
        """, (resultado, data_result, req_id))


def eliminar_requisicao(req_id):
    """Remove uma requisição pelo ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM lab_requisicoes WHERE id = ?", (req_id,))


# ─── ESTATÍSTICAS ─────────────────────────────────────────────────────────────

def estatisticas_lab(inicio, fim):
    """
    Devolve estatísticas do laboratório para o período indicado.
    Retorna: total, pendentes, concluidos, urgentes.
    """
    with db.get_conn() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM lab_requisicoes WHERE data_req BETWEEN ? AND ?",
            (inicio, fim)
        ).fetchone()[0]

        pendentes = conn.execute(
            "SELECT COUNT(*) FROM lab_requisicoes WHERE data_req BETWEEN ? AND ? AND estado = 'pendente'",
            (inicio, fim)
        ).fetchone()[0]

        concluidos = conn.execute(
            "SELECT COUNT(*) FROM lab_requisicoes WHERE data_req BETWEEN ? AND ? AND estado = 'concluido'",
            (inicio, fim)
        ).fetchone()[0]

        urgentes = conn.execute(
            "SELECT COUNT(*) FROM lab_requisicoes WHERE data_req BETWEEN ? AND ? AND urgente = 1",
            (inicio, fim)
        ).fetchone()[0]

    return {
        'total':      total,
        'pendentes':  pendentes,
        'concluidos': concluidos,
        'urgentes':   urgentes,
    }
