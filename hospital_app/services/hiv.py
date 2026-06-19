"""
hiv.py — Funções CRUD para o serviço de VIH / SIDA
Tabelas: hiv_pacientes, hiv_consultas
"""

import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── PACIENTES ────────────────────────────────────────────────────────────────

def listar_pacientes(activo=True):
    """
    Devolve a lista de pacientes VIH.
    Por defeito apenas pacientes activos (activo=1).
    """
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM hiv_pacientes WHERE activo = ? ORDER BY nome",
            (1 if activo else 0,)
        ).fetchall()
    return db.linhas_para_lista(rows)


def criar_paciente(dados):
    """
    Regista um novo paciente VIH.
    Gera ID com prefixo 'H'. Devolve o ID criado.
    """
    novo_id = 'H' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO hiv_pacientes
                (id, nome, nup, sexo, data_nasc, data_diag, estadio,
                 tarv, regimen_tarv, data_inicio_tarv, hospital, activo, criado)
            VALUES
                (:id, :nome, :nup, :sexo, :data_nasc, :data_diag, :estadio,
                 :tarv, :regimen_tarv, :data_inicio_tarv, :hospital, 1, :agora)
        """, {
            'id':              novo_id,
            'nome':            dados.get('nome', ''),
            'nup':             dados.get('nup', ''),
            'sexo':            dados.get('sexo', ''),
            'data_nasc':       dados.get('data_nasc', ''),
            'data_diag':       dados.get('data_diag', ''),
            'estadio':         dados.get('estadio', ''),
            'tarv':            int(dados.get('tarv', 0)),
            'regimen_tarv':    dados.get('regimen_tarv', ''),
            'data_inicio_tarv': dados.get('data_inicio_tarv', ''),
            'hospital':        dados.get('hospital', ''),
            'agora':           agora,
        })
    return novo_id


def actualizar_paciente(pid, dados):
    """Actualiza os dados clínicos de um paciente VIH existente."""
    with db.get_conn() as conn:
        conn.execute("""
            UPDATE hiv_pacientes
            SET nome=:nome, nup=:nup, sexo=:sexo, data_nasc=:data_nasc,
                data_diag=:data_diag, estadio=:estadio, tarv=:tarv,
                regimen_tarv=:regimen_tarv, data_inicio_tarv=:data_inicio_tarv,
                hospital=:hospital
            WHERE id=:id
        """, {
            'id':              pid,
            'nome':            dados.get('nome', ''),
            'nup':             dados.get('nup', ''),
            'sexo':            dados.get('sexo', ''),
            'data_nasc':       dados.get('data_nasc', ''),
            'data_diag':       dados.get('data_diag', ''),
            'estadio':         dados.get('estadio', ''),
            'tarv':            int(dados.get('tarv', 0)),
            'regimen_tarv':    dados.get('regimen_tarv', ''),
            'data_inicio_tarv': dados.get('data_inicio_tarv', ''),
            'hospital':        dados.get('hospital', ''),
        })


def eliminar_paciente(pid):
    """
    Desactiva um paciente (soft delete: activo=0).
    O registo é mantido na base de dados.
    """
    with db.get_conn() as conn:
        conn.execute(
            "UPDATE hiv_pacientes SET activo = 0 WHERE id = ?", (pid,)
        )


# ─── CONSULTAS ────────────────────────────────────────────────────────────────

def listar_consultas(paciente_id=None, data_inicio=None, data_fim=None):
    """
    Devolve a lista de consultas VIH.
    Filtros opcionais: paciente_id e/ou intervalo de datas.
    """
    sql = "SELECT * FROM hiv_consultas WHERE 1=1"
    params = []

    if paciente_id:
        sql += " AND paciente_id = ?"
        params.append(paciente_id)

    if data_inicio and data_fim:
        sql += " AND data_consulta BETWEEN ? AND ?"
        params += [data_inicio, data_fim]
    elif data_inicio:
        sql += " AND data_consulta >= ?"
        params.append(data_inicio)
    elif data_fim:
        sql += " AND data_consulta <= ?"
        params.append(data_fim)

    sql += " ORDER BY data_consulta DESC"

    with db.get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return db.linhas_para_lista(rows)


def registar_consulta(dados):
    """
    Regista uma nova consulta de seguimento VIH.
    Gera ID com prefixo 'C'. Devolve o ID criado.
    """
    novo_id = 'C' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO hiv_consultas
                (id, paciente_id, data_consulta, peso, cd4, carga_viral,
                 estadio, tarv_actual, observacoes, criado)
            VALUES
                (:id, :paciente_id, :data_consulta, :peso, :cd4, :carga_viral,
                 :estadio, :tarv_actual, :observacoes, :agora)
        """, {
            'id':            novo_id,
            'paciente_id':   dados.get('paciente_id', ''),
            'data_consulta': dados.get('data_consulta', datetime.today().strftime('%Y-%m-%d')),
            'peso':          dados.get('peso'),
            'cd4':           dados.get('cd4'),
            'carga_viral':   dados.get('carga_viral', ''),
            'estadio':       dados.get('estadio', ''),
            'tarv_actual':   dados.get('tarv_actual', ''),
            'observacoes':   dados.get('observacoes', ''),
            'agora':         agora,
        })
    return novo_id


def eliminar_consulta(cid):
    """Remove um registo de consulta VIH pelo ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM hiv_consultas WHERE id = ?", (cid,))


# ─── ESTATÍSTICAS ─────────────────────────────────────────────────────────────

def estatisticas_hiv():
    """
    Devolve estatísticas gerais do serviço VIH.
    Retorna: total_pacientes, em_tarv, sem_tarv, consultas_mes (mês actual).
    """
    hoje = datetime.today()
    inicio_mes = hoje.strftime('%Y-%m-01')
    fim_mes = hoje.strftime('%Y-%m-') + str(hoje.day).zfill(2)

    with db.get_conn() as conn:
        total_pacientes = conn.execute(
            "SELECT COUNT(*) FROM hiv_pacientes WHERE activo = 1"
        ).fetchone()[0]

        em_tarv = conn.execute(
            "SELECT COUNT(*) FROM hiv_pacientes WHERE activo = 1 AND tarv = 1"
        ).fetchone()[0]

        sem_tarv = conn.execute(
            "SELECT COUNT(*) FROM hiv_pacientes WHERE activo = 1 AND tarv = 0"
        ).fetchone()[0]

        consultas_mes = conn.execute(
            "SELECT COUNT(*) FROM hiv_consultas WHERE data_consulta BETWEEN ? AND ?",
            (inicio_mes, fim_mes)
        ).fetchone()[0]

    return {
        'total_pacientes': total_pacientes,
        'em_tarv':         em_tarv,
        'sem_tarv':        sem_tarv,
        'consultas_mes':   consultas_mes,
    }
