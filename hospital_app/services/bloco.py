"""
bloco.py — Funções CRUD para o Bloco Operatório
Tabela principal: bloco_cirurgias
"""

import sys
import os
import uuid

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import database as db


# ─── LISTAR ──────────────────────────────────────────────────────────────────

def listar_cirurgias(data=None, estado=None, urgencia=None):
    """
    Devolve a lista de cirurgias com filtros opcionais.
    - data: data única (YYYY-MM-DD) ou lista/tuplo [data_inicio, data_fim]
    - estado: agendada, em_curso, concluida, cancelada
    - urgencia: electiva, urgente, emergencia
    """
    query = "SELECT * FROM bloco_cirurgias WHERE 1=1"
    params = []

    if data:
        # Aceita intervalo [data_inicio, data_fim] ou data única
        if isinstance(data, (list, tuple)) and len(data) == 2:
            query += " AND data_prog BETWEEN ? AND ?"
            params.extend(data)
        else:
            query += " AND data_prog = ?"
            params.append(data)

    if estado:
        query += " AND estado = ?"
        params.append(estado)

    if urgencia:
        query += " AND urgencia = ?"
        params.append(urgencia)

    query += " ORDER BY data_prog DESC, hora_inicio ASC"

    with db.get_conn() as conn:
        rows = conn.execute(query, params).fetchall()

    return db.linhas_para_lista(rows)


# ─── CRIAR ───────────────────────────────────────────────────────────────────

def criar_cirurgia(dados):
    """
    Insere uma nova cirurgia na base de dados.
    ID gerado automaticamente com prefixo 'B'.
    Devolve o ID do novo registo.
    """
    novo_id = 'B' + str(uuid.uuid4())[:7].upper()

    with db.get_conn() as conn:
        conn.execute("""
            INSERT INTO bloco_cirurgias
                (id, nome, nup, sexo, idade, tipo_cirurgia, urgencia, cirurgiao,
                 anestesista, anestesia, data_prog, hora_inicio, sala, diagnostico, estado)
            VALUES
                (:id, :nome, :nup, :sexo, :idade, :tipo_cirurgia, :urgencia, :cirurgiao,
                 :anestesista, :anestesia, :data_prog, :hora_inicio, :sala, :diagnostico, :estado)
        """, {
            'id':           novo_id,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'tipo_cirurgia': dados.get('tipo_cirurgia', ''),
            'urgencia':     dados.get('urgencia', 'electiva'),
            'cirurgiao':    dados.get('cirurgiao', ''),
            'anestesista':  dados.get('anestesista', ''),
            'anestesia':    dados.get('anestesia', ''),
            'data_prog':    dados.get('data_prog', ''),
            'hora_inicio':  dados.get('hora_inicio', ''),
            'sala':         dados.get('sala', ''),
            'diagnostico':  dados.get('diagnostico', ''),
            'estado':       dados.get('estado', 'agendada'),
        })

    return novo_id


# ─── ACTUALIZAR ──────────────────────────────────────────────────────────────

def actualizar_cirurgia(bid, dados):
    """
    Actualiza os dados de uma cirurgia existente.
    Permite actualizar todos os campos incluindo estado, hora_fim e complicacoes.
    """
    with db.get_conn() as conn:
        conn.execute("""
            UPDATE bloco_cirurgias
            SET nome         = :nome,
                nup          = :nup,
                sexo         = :sexo,
                idade        = :idade,
                tipo_cirurgia = :tipo_cirurgia,
                urgencia     = :urgencia,
                cirurgiao    = :cirurgiao,
                anestesista  = :anestesista,
                anestesia    = :anestesia,
                data_prog    = :data_prog,
                hora_inicio  = :hora_inicio,
                hora_fim     = :hora_fim,
                sala         = :sala,
                estado       = :estado,
                diagnostico  = :diagnostico,
                complicacoes = :complicacoes,
                observacoes  = :observacoes
            WHERE id = :id
        """, {
            'id':           bid,
            'nome':         dados.get('nome', ''),
            'nup':          dados.get('nup', ''),
            'sexo':         dados.get('sexo', ''),
            'idade':        dados.get('idade'),
            'tipo_cirurgia': dados.get('tipo_cirurgia', ''),
            'urgencia':     dados.get('urgencia', 'electiva'),
            'cirurgiao':    dados.get('cirurgiao', ''),
            'anestesista':  dados.get('anestesista', ''),
            'anestesia':    dados.get('anestesia', ''),
            'data_prog':    dados.get('data_prog', ''),
            'hora_inicio':  dados.get('hora_inicio', ''),
            'hora_fim':     dados.get('hora_fim', ''),
            'sala':         dados.get('sala', ''),
            'estado':       dados.get('estado', 'agendada'),
            'diagnostico':  dados.get('diagnostico', ''),
            'complicacoes': dados.get('complicacoes', ''),
            'observacoes':  dados.get('observacoes', ''),
        })


# ─── ELIMINAR ────────────────────────────────────────────────────────────────

def eliminar_cirurgia(bid):
    """Remove uma cirurgia pelo seu ID."""
    with db.get_conn() as conn:
        conn.execute("DELETE FROM bloco_cirurgias WHERE id = ?", (bid,))


# ─── ESTATÍSTICAS ────────────────────────────────────────────────────────────

def estatisticas_bloco(data_inicio, data_fim):
    """
    Calcula estatísticas das cirurgias num intervalo de datas.
    Devolve um dicionário com:
    - total: número total de cirurgias
    - electivas, urgentes, emergencias: contagens por urgencia
    - concluidas, canceladas: contagens por estado
    """
    with db.get_conn() as conn:
        # Totais por nível de urgência
        rows_urgencia = conn.execute("""
            SELECT urgencia, COUNT(*) AS total
            FROM bloco_cirurgias
            WHERE data_prog BETWEEN ? AND ?
            GROUP BY urgencia
        """, (data_inicio, data_fim)).fetchall()

        # Totais por estado
        rows_estado = conn.execute("""
            SELECT estado, COUNT(*) AS total
            FROM bloco_cirurgias
            WHERE data_prog BETWEEN ? AND ?
            GROUP BY estado
        """, (data_inicio, data_fim)).fetchall()

    # Agregar resultados
    por_urgencia = {r['urgencia']: r['total'] for r in rows_urgencia}
    por_estado   = {r['estado']:   r['total'] for r in rows_estado}
    total = sum(por_urgencia.values())

    return {
        'total':       total,
        'electivas':   por_urgencia.get('electiva', 0),
        'urgentes':    por_urgencia.get('urgente', 0),
        'emergencias': por_urgencia.get('emergencia', 0),
        'concluidas':  por_estado.get('concluida', 0),
        'canceladas':  por_estado.get('cancelada', 0),
    }
