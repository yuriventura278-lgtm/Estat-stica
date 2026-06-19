"""
hemoterapia.py — Funções CRUD para o serviço de Hemoterapia
Tabelas: hemo_dadores, hemo_transfusoes, hemo_stock
"""

import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── DADORES / DÁDIVAS ────────────────────────────────────────────────────────

def listar_dadores(data_inicio=None, data_fim=None):
    """
    Devolve a lista de dádivas registadas.
    Filtro opcional por intervalo de datas.
    """
    sql = "SELECT * FROM hemo_dadores WHERE 1=1"
    params = []

    if data_inicio and data_fim:
        sql += " AND data_dadiva BETWEEN ? AND ?"
        params += [data_inicio, data_fim]
    elif data_inicio:
        sql += " AND data_dadiva >= ?"
        params.append(data_inicio)
    elif data_fim:
        sql += " AND data_dadiva <= ?"
        params.append(data_fim)

    sql += " ORDER BY data_dadiva DESC"

    with db.get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return db.linhas_para_lista(rows)


def registar_dadiva(dados):
    """
    Regista uma nova dádiva de sangue.
    Gera ID com prefixo 'D'.
    Se o estado for 'aprovado', adiciona unidades ao stock (volume_ml / 450, arredondado).
    Devolve o ID criado.
    """
    novo_id = 'D' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')
    estado = dados.get('estado', 'aprovado')
    volume_ml = int(dados.get('volume_ml', 450))
    grupo_sang = dados.get('grupo_sang', '')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO hemo_dadores
                (id, nome, nup, sexo, idade, grupo_sang, data_dadiva,
                 volume_ml, estado, observacoes, criado)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :grupo_sang, :data_dadiva,
                 :volume_ml, :estado, :observacoes, :agora)
        """, {
            'id':          novo_id,
            'nome':        dados.get('nome', ''),
            'nup':         dados.get('nup', ''),
            'sexo':        dados.get('sexo', ''),
            'idade':       dados.get('idade'),
            'grupo_sang':  grupo_sang,
            'data_dadiva': dados.get('data_dadiva', datetime.today().strftime('%Y-%m-%d')),
            'volume_ml':   volume_ml,
            'estado':      estado,
            'observacoes': dados.get('observacoes', ''),
            'agora':       agora,
        })

        # Actualiza o stock se a dádiva for aprovada
        if estado == 'aprovado' and grupo_sang:
            unidades = round(volume_ml / 450)
            conn.execute("""
                UPDATE hemo_stock
                SET quantidade = quantidade + ?, actualizado = ?
                WHERE grupo_sang = ?
            """, (unidades, agora, grupo_sang))

    return novo_id


def eliminar_dadiva(did):
    """
    Remove uma dádiva pelo ID.
    Se estava aprovada, subtrai as unidades correspondentes do stock.
    """
    agora = datetime.now().isoformat(timespec='seconds')

    with db.get_conn() as conn:
        # Verificar se a dádiva existe e se estava aprovada
        row = conn.execute(
            "SELECT estado, grupo_sang, volume_ml FROM hemo_dadores WHERE id = ?", (did,)
        ).fetchone()

        if row:
            conn.execute("DELETE FROM hemo_dadores WHERE id = ?", (did,))

            # Subtrair do stock se estava aprovada
            if row['estado'] == 'aprovado' and row['grupo_sang']:
                unidades = round(row['volume_ml'] / 450)
                conn.execute("""
                    UPDATE hemo_stock
                    SET quantidade = MAX(0, quantidade - ?), actualizado = ?
                    WHERE grupo_sang = ?
                """, (unidades, agora, row['grupo_sang']))


# ─── TRANSFUSÕES ─────────────────────────────────────────────────────────────

def listar_transfusoes(data_inicio=None, data_fim=None):
    """
    Devolve a lista de transfusões registadas.
    Filtro opcional por intervalo de datas.
    """
    sql = "SELECT * FROM hemo_transfusoes WHERE 1=1"
    params = []

    if data_inicio and data_fim:
        sql += " AND data_transf BETWEEN ? AND ?"
        params += [data_inicio, data_fim]
    elif data_inicio:
        sql += " AND data_transf >= ?"
        params.append(data_inicio)
    elif data_fim:
        sql += " AND data_transf <= ?"
        params.append(data_fim)

    sql += " ORDER BY data_transf DESC"

    with db.get_conn() as conn:
        rows = conn.execute(sql, params).fetchall()
    return db.linhas_para_lista(rows)


def registar_transfusao(dados):
    """
    Regista uma transfusão de sangue.
    Gera ID com prefixo 'T'.
    Subtrai 1 unidade do stock para o grupo sanguíneo indicado.
    Devolve o ID criado.
    """
    novo_id = 'T' + str(uuid.uuid4())[:7].upper()
    agora = datetime.now().isoformat(timespec='seconds')
    grupo_sang = dados.get('grupo_sang', '')

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO hemo_transfusoes
                (id, nome_receptor, nup_receptor, grupo_sang, volume_ml,
                 indicacao, medico, data_transf, reacao, observacoes, criado)
            VALUES
                (:id, :nome_receptor, :nup_receptor, :grupo_sang, :volume_ml,
                 :indicacao, :medico, :data_transf, :reacao, :observacoes, :agora)
        """, {
            'id':            novo_id,
            'nome_receptor': dados.get('nome_receptor', ''),
            'nup_receptor':  dados.get('nup_receptor', ''),
            'grupo_sang':    grupo_sang,
            'volume_ml':     dados.get('volume_ml'),
            'indicacao':     dados.get('indicacao', ''),
            'medico':        dados.get('medico', ''),
            'data_transf':   dados.get('data_transf', datetime.today().strftime('%Y-%m-%d')),
            'reacao':        dados.get('reacao', 'nenhuma'),
            'observacoes':   dados.get('observacoes', ''),
            'agora':         agora,
        })

        # Subtrai 1 unidade do stock para o grupo sanguíneo
        if grupo_sang:
            conn.execute("""
                UPDATE hemo_stock
                SET quantidade = MAX(0, quantidade - 1), actualizado = ?
                WHERE grupo_sang = ?
            """, (agora, grupo_sang))

    return novo_id


def eliminar_transfusao(tid):
    """Remove um registo de transfusão pelo ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM hemo_transfusoes WHERE id = ?", (tid,))


# ─── STOCK ───────────────────────────────────────────────────────────────────

def obter_stock():
    """Devolve a lista de todos os grupos sanguíneos com as quantidades em stock."""
    with db.get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM hemo_stock ORDER BY grupo_sang"
        ).fetchall()
    return db.linhas_para_lista(rows)


# ─── ESTATÍSTICAS ─────────────────────────────────────────────────────────────

def estatisticas_hemo(inicio, fim):
    """
    Devolve estatísticas do serviço de hemoterapia para o período indicado.
    Retorna: total_dadivas, total_transfusoes, stock_critico (grupos com qty < 2).
    """
    with db.get_conn() as conn:
        total_dadivas = conn.execute(
            "SELECT COUNT(*) FROM hemo_dadores WHERE data_dadiva BETWEEN ? AND ?",
            (inicio, fim)
        ).fetchone()[0]

        total_transfusoes = conn.execute(
            "SELECT COUNT(*) FROM hemo_transfusoes WHERE data_transf BETWEEN ? AND ?",
            (inicio, fim)
        ).fetchone()[0]

        # Grupos com stock crítico (menos de 2 unidades)
        rows_critico = conn.execute(
            "SELECT grupo_sang FROM hemo_stock WHERE quantidade < 2 ORDER BY grupo_sang"
        ).fetchall()
        stock_critico = [r['grupo_sang'] for r in rows_critico]

    return {
        'total_dadivas':      total_dadivas,
        'total_transfusoes':  total_transfusoes,
        'stock_critico':      stock_critico,
    }
