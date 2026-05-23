"""
app.py — Servidor Flask do Sistema de Gestão do Hospital do Prenda
Executa com:  python app.py
Acede em:     http://localhost:5000
"""

import os, json
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for

import database as db
import auth

# Módulos de serviço
import services.laboratorio as lab
import services.hiv         as hiv
import services.hemoterapia as hemo
import services.imagiologia as imag
import services.consulta    as con
import services.bloco       as bloco
import services.fisioterapia as fisio

# ─── CONFIGURAÇÃO ────────────────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'hprenda-2026-chave-secreta-mudar-em-producao')

db.criar_tabelas()
auth.garantir_admin_padrao()


# ─── UTILITÁRIOS ─────────────────────────────────────────────────────────────

def hoje():
    return date.today().isoformat()

def ok(dados=None, msg='Operação realizada com sucesso'):
    return jsonify({'ok': True, 'mensagem': msg, 'dados': dados})

def erro(msg, codigo=400):
    return jsonify({'ok': False, 'mensagem': msg}), codigo

def ctx():
    """Contexto base para todos os templates (utilizador autenticado)."""
    return {'utilizador': auth.utilizador_actual(), 'hoje': hoje()}


# ─── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

@app.route('/login', methods=['GET', 'POST'])
def pagina_login():
    if 'user_id' in session:
        return redirect(url_for('pagina_inicio'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        senha    = request.form.get('senha', '')
        next_url = request.form.get('next', '/')

        u = auth.autenticar(username, senha)
        if not u:
            return render_template('auth/login.html',
                erro='Utilizador ou senha incorrectos.',
                username_prev=username, next=next_url)

        session['user_id'] = u['id']
        session.permanent = True

        # Forçar alteração de senha na primeira sessão
        if u['primeira_sessao']:
            return redirect(url_for('pagina_alterar_senha'))

        return redirect(next_url if next_url.startswith('/') else '/')

    return render_template('auth/login.html',
        next=request.args.get('next', '/'))


@app.route('/logout')
def pagina_logout():
    session.clear()
    return redirect(url_for('pagina_login'))


@app.route('/alterar-senha', methods=['GET', 'POST'])
@auth.login_required
def pagina_alterar_senha():
    u = auth.utilizador_actual()

    if request.method == 'POST':
        senha_nova      = request.form.get('senha_nova', '')
        senha_confirmar = request.form.get('senha_confirmar', '')
        senha_actual    = request.form.get('senha_actual', '')

        if len(senha_nova) < 6:
            return render_template('auth/alterar_senha.html',
                erro='A nova senha deve ter pelo menos 6 caracteres.',
                primeira_sessao=u['primeira_sessao'])

        if senha_nova != senha_confirmar:
            return render_template('auth/alterar_senha.html',
                erro='As senhas não coincidem.',
                primeira_sessao=u['primeira_sessao'])

        if not u['primeira_sessao']:
            if not auth.verificar_senha(senha_actual, u['password_hash']):
                return render_template('auth/alterar_senha.html',
                    erro='Senha actual incorrecta.',
                    primeira_sessao=False)

        auth.alterar_senha(u['id'], senha_nova)
        return redirect(url_for('pagina_inicio'))

    return render_template('auth/alterar_senha.html',
        primeira_sessao=u['primeira_sessao'])


# ─── GESTÃO DE UTILIZADORES (só admins) ──────────────────────────────────────

@app.route('/admin/utilizadores')
@auth.login_required
def pagina_utilizadores():
    u = auth.utilizador_actual()
    if u['cargo'] != 'admin':
        return redirect('/')
    lista = auth.listar_utilizadores()
    return render_template('admin/utilizadores.html', utilizadores=lista, **ctx())


@app.route('/api/admin/utilizadores', methods=['POST'])
@auth.login_required
def api_criar_utilizador():
    u = auth.utilizador_actual()
    if u['cargo'] != 'admin':
        return erro('Sem permissão', 403)
    d = request.get_json()
    try:
        auth.criar_utilizador(d['username'], d['nome_completo'], d['senha'],
                              d.get('cargo','enfermeiro'), d.get('servico','geral'))
        return ok(msg='Utilizador criado com sucesso')
    except ValueError as e:
        return erro(str(e))


@app.route('/api/admin/utilizadores/<int:uid>', methods=['DELETE'])
@auth.login_required
def api_desactivar_utilizador(uid):
    u = auth.utilizador_actual()
    if u['cargo'] != 'admin':
        return erro('Sem permissão', 403)
    auth.desactivar_utilizador(uid)
    return ok(msg='Utilizador desactivado')


# ─── PÁGINAS PRINCIPAIS ───────────────────────────────────────────────────────

@app.route('/')
@auth.login_required
def pagina_inicio():
    return render_template('index.html', **ctx())


@app.route('/cirurgia')
@auth.login_required
def pagina_cirurgia():
    data = request.args.get('data', hoje())
    return render_template('cirurgia/index.html',
        data=data, hospitais=db.listar_hospitais(), **ctx())


@app.route('/laboratorio')
@auth.login_required
def pagina_laboratorio():
    data = request.args.get('data', hoje())
    return render_template('laboratorio/index.html', data=data, **ctx())


@app.route('/hiv')
@auth.login_required
def pagina_hiv():
    return render_template('hiv/index.html',
        hospitais=db.listar_hospitais(), **ctx())


@app.route('/hemoterapia')
@auth.login_required
def pagina_hemoterapia():
    data = request.args.get('data', hoje())
    return render_template('hemoterapia/index.html', data=data, **ctx())


@app.route('/imagiologia')
@auth.login_required
def pagina_imagiologia():
    data = request.args.get('data', hoje())
    return render_template('imagiologia/index.html', data=data, **ctx())


@app.route('/consulta')
@auth.login_required
def pagina_consulta():
    data = request.args.get('data', hoje())
    return render_template('consulta/index.html', data=data, **ctx())


@app.route('/bloco')
@auth.login_required
def pagina_bloco():
    data = request.args.get('data', hoje())
    return render_template('bloco/index.html', data=data, **ctx())


@app.route('/fisioterapia')
@auth.login_required
def pagina_fisioterapia():
    return render_template('fisioterapia/index.html', **ctx())


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — CIRURGIA ───────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/cirurgia/doentes', methods=['GET'])
@auth.login_required
def api_cir_listar():
    return ok(db.listar_doentes_internados(request.args.get('data')))

@app.route('/api/cirurgia/doentes', methods=['POST'])
@auth.login_required
def api_cir_criar():
    d = request.get_json()
    if not d.get('nome'):  return erro('Campo obrigatório: Nome')
    if not d.get('sexo'):  return erro('Campo obrigatório: Sexo')
    if not d.get('nup'):   return erro('Campo obrigatório: NUP')
    return ok({'id': db.criar_doente(d)}, 'Doente registado com sucesso')

@app.route('/api/cirurgia/doentes/<did>', methods=['PUT'])
@auth.login_required
def api_cir_actualizar(did):
    if not db.obter_doente(did): return erro('Doente não encontrado', 404)
    db.actualizar_doente(did, request.get_json())
    return ok(msg='Doente actualizado com sucesso')

@app.route('/api/cirurgia/doentes/<did>', methods=['DELETE'])
@auth.login_required
def api_cir_eliminar(did):
    if not db.obter_doente(did): return erro('Doente não encontrado', 404)
    db.eliminar_doente(did)
    return ok(msg='Doente eliminado com sucesso')

@app.route('/api/cirurgia/altas', methods=['GET'])
@auth.login_required
def api_cir_altas_listar():
    return ok(db.listar_altas(request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/cirurgia/altas', methods=['POST'])
@auth.login_required
def api_cir_alta():
    d = request.get_json()
    if not d.get('doente_id'):  return erro('Campo obrigatório: doente_id')
    if not d.get('data_saida'): return erro('Campo obrigatório: data_saida')
    if not d.get('diag_fim'):   return erro('Campo obrigatório: diagnóstico final')
    try:
        return ok({'id': db.registar_alta(d['doente_id'], d)}, 'Alta registada com sucesso')
    except ValueError as e:
        return erro(str(e), 404)

@app.route('/api/cirurgia/altas/<aid>', methods=['DELETE'])
@auth.login_required
def api_cir_alta_del(aid):
    db.eliminar_alta(aid)
    return ok(msg='Alta eliminada com sucesso')

@app.route('/api/cirurgia/obitos', methods=['GET'])
@auth.login_required
def api_cir_obitos_listar():
    return ok(db.listar_obitos(request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/cirurgia/obitos', methods=['POST'])
@auth.login_required
def api_cir_obito():
    d = request.get_json()
    if not d.get('nome'):       return erro('Campo obrigatório: Nome')
    if not d.get('data_obito'): return erro('Campo obrigatório: Data do óbito')
    return ok({'id': db.registar_obito(d)}, 'Óbito registado com sucesso')

@app.route('/api/cirurgia/obitos/<oid>', methods=['DELETE'])
@auth.login_required
def api_cir_obito_del(oid):
    db.eliminar_obito(oid)
    return ok(msg='Óbito eliminado com sucesso')

@app.route('/api/cirurgia/camas', methods=['GET'])
@auth.login_required
def api_cir_camas_get():
    data = request.args.get('data', hoje())
    return ok({'data': data, 'camas': db.obter_camas(data)})

@app.route('/api/cirurgia/camas', methods=['POST'])
@auth.login_required
def api_cir_camas_set():
    d = request.get_json()
    camas = d.get('camas', 0)
    if not isinstance(camas, int) or camas < 0: return erro('Número inválido')
    db.guardar_camas(d.get('data', hoje()), camas)
    return ok(msg=f'Camas guardadas: {camas}')

@app.route('/api/cirurgia/estatisticas', methods=['GET'])
@auth.login_required
def api_cir_stats():
    data = request.args.get('data', hoje())
    inicio = request.args.get('inicio', data[:7]+'-01')
    fim    = request.args.get('fim', data)
    internados = db.listar_doentes_internados(data)
    altas  = db.listar_altas(inicio, fim)
    obitos = db.listar_obitos(inicio, fim)
    camas  = db.obter_camas(data)
    total_saidas = len(altas) + len(obitos)
    taxa = round(len(obitos)/total_saidas*100, 1) if total_saidas > 0 else 0
    return ok({'data':data,'internados':len(internados),'altas':len(altas),
               'obitos':len(obitos),'camas':camas,'taxa_mortalidade':taxa})

@app.route('/api/cirurgia/exportar')
@auth.login_required
def api_cir_exportar():
    dados = db.exportar_json('cirurgia')
    nome = f"backup_cirurgia_{hoje()}.json"
    caminho = os.path.join(os.path.dirname(__file__), 'exports', nome)
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return send_file(caminho, as_attachment=True, download_name=nome)


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — LABORATÓRIO ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/lab/requisicoes', methods=['GET'])
@auth.login_required
def api_lab_listar():
    return ok(lab.listar_requisicoes(
        request.args.get('inicio'), request.args.get('fim'),
        request.args.get('estado')))

@app.route('/api/lab/requisicoes', methods=['POST'])
@auth.login_required
def api_lab_criar():
    d = request.get_json()
    if not d.get('nome'):          return erro('Campo obrigatório: Nome')
    if not d.get('tipo_analise'):  return erro('Campo obrigatório: Tipo de análise')
    if not d.get('data_req'):      return erro('Campo obrigatório: Data')
    return ok({'id': lab.criar_requisicao(d)}, 'Requisição criada com sucesso')

@app.route('/api/lab/requisicoes/<rid>/resultado', methods=['PUT'])
@auth.login_required
def api_lab_resultado(rid):
    d = request.get_json()
    if not d.get('resultado'): return erro('Campo obrigatório: Resultado')
    lab.actualizar_resultado(rid, d['resultado'], d.get('data_result'))
    return ok(msg='Resultado registado com sucesso')

@app.route('/api/lab/requisicoes/<rid>', methods=['DELETE'])
@auth.login_required
def api_lab_del(rid):
    lab.eliminar_requisicao(rid)
    return ok(msg='Requisição eliminada com sucesso')

@app.route('/api/lab/estatisticas', methods=['GET'])
@auth.login_required
def api_lab_stats():
    data = request.args.get('data', hoje())
    return ok(lab.estatisticas_lab(data[:7]+'-01', data))


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — VIH / SIDA ────────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/hiv/pacientes', methods=['GET'])
@auth.login_required
def api_hiv_listar():
    return ok(hiv.listar_pacientes())

@app.route('/api/hiv/pacientes', methods=['POST'])
@auth.login_required
def api_hiv_criar():
    d = request.get_json()
    if not d.get('nome'): return erro('Campo obrigatório: Nome')
    return ok({'id': hiv.criar_paciente(d)}, 'Paciente registado com sucesso')

@app.route('/api/hiv/pacientes/<pid>', methods=['PUT'])
@auth.login_required
def api_hiv_actualizar(pid):
    hiv.actualizar_paciente(pid, request.get_json())
    return ok(msg='Paciente actualizado com sucesso')

@app.route('/api/hiv/pacientes/<pid>', methods=['DELETE'])
@auth.login_required
def api_hiv_del(pid):
    hiv.eliminar_paciente(pid)
    return ok(msg='Paciente desactivado com sucesso')

@app.route('/api/hiv/consultas', methods=['GET'])
@auth.login_required
def api_hiv_consultas():
    return ok(hiv.listar_consultas(
        request.args.get('paciente_id'),
        request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/hiv/consultas', methods=['POST'])
@auth.login_required
def api_hiv_consulta():
    d = request.get_json()
    if not d.get('paciente_id'):    return erro('Campo obrigatório: paciente_id')
    if not d.get('data_consulta'):  return erro('Campo obrigatório: Data')
    return ok({'id': hiv.registar_consulta(d)}, 'Consulta registada com sucesso')

@app.route('/api/hiv/consultas/<cid>', methods=['DELETE'])
@auth.login_required
def api_hiv_consulta_del(cid):
    hiv.eliminar_consulta(cid)
    return ok(msg='Consulta eliminada com sucesso')

@app.route('/api/hiv/estatisticas', methods=['GET'])
@auth.login_required
def api_hiv_stats():
    return ok(hiv.estatisticas_hiv())


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — HEMOTERAPIA ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/hemo/dadores', methods=['GET'])
@auth.login_required
def api_hemo_dadores():
    return ok(hemo.listar_dadores(request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/hemo/dadores', methods=['POST'])
@auth.login_required
def api_hemo_dadiva():
    d = request.get_json()
    if not d.get('nome'):       return erro('Campo obrigatório: Nome')
    if not d.get('grupo_sang'): return erro('Campo obrigatório: Grupo Sanguíneo')
    if not d.get('data_dadiva'):return erro('Campo obrigatório: Data')
    return ok({'id': hemo.registar_dadiva(d)}, 'Dádiva registada com sucesso')

@app.route('/api/hemo/dadores/<did>', methods=['DELETE'])
@auth.login_required
def api_hemo_dadiva_del(did):
    hemo.eliminar_dadiva(did)
    return ok(msg='Dádiva eliminada com sucesso')

@app.route('/api/hemo/transfusoes', methods=['GET'])
@auth.login_required
def api_hemo_transf():
    return ok(hemo.listar_transfusoes(request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/hemo/transfusoes', methods=['POST'])
@auth.login_required
def api_hemo_transf_criar():
    d = request.get_json()
    if not d.get('nome_receptor'): return erro('Campo obrigatório: Nome do receptor')
    if not d.get('grupo_sang'):    return erro('Campo obrigatório: Grupo sanguíneo')
    if not d.get('data_transf'):   return erro('Campo obrigatório: Data')
    return ok({'id': hemo.registar_transfusao(d)}, 'Transfusão registada com sucesso')

@app.route('/api/hemo/transfusoes/<tid>', methods=['DELETE'])
@auth.login_required
def api_hemo_transf_del(tid):
    hemo.eliminar_transfusao(tid)
    return ok(msg='Transfusão eliminada com sucesso')

@app.route('/api/hemo/stock', methods=['GET'])
@auth.login_required
def api_hemo_stock():
    return ok(hemo.obter_stock())

@app.route('/api/hemo/estatisticas', methods=['GET'])
@auth.login_required
def api_hemo_stats():
    data = request.args.get('data', hoje())
    return ok(hemo.estatisticas_hemo(data[:7]+'-01', data))


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — IMAGIOLOGIA ───────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/imag/exames', methods=['GET'])
@auth.login_required
def api_imag_listar():
    return ok(imag.listar_exames(
        request.args.get('inicio'), request.args.get('fim'),
        request.args.get('estado'), request.args.get('tipo')))

@app.route('/api/imag/exames', methods=['POST'])
@auth.login_required
def api_imag_criar():
    d = request.get_json()
    if not d.get('nome'):       return erro('Campo obrigatório: Nome')
    if not d.get('tipo_exame'): return erro('Campo obrigatório: Tipo de exame')
    if not d.get('data_req'):   return erro('Campo obrigatório: Data')
    return ok({'id': imag.criar_exame(d)}, 'Exame criado com sucesso')

@app.route('/api/imag/exames/<eid>/resultado', methods=['PUT'])
@auth.login_required
def api_imag_resultado(eid):
    d = request.get_json()
    if not d.get('resultado'): return erro('Campo obrigatório: Resultado')
    imag.actualizar_resultado(eid, d['resultado'], d.get('conclusao',''), d.get('data_result'))
    return ok(msg='Resultado registado com sucesso')

@app.route('/api/imag/exames/<eid>', methods=['DELETE'])
@auth.login_required
def api_imag_del(eid):
    imag.eliminar_exame(eid)
    return ok(msg='Exame eliminado com sucesso')

@app.route('/api/imag/estatisticas', methods=['GET'])
@auth.login_required
def api_imag_stats():
    data = request.args.get('data', hoje())
    return ok(imag.estatisticas_imag(data[:7]+'-01', data))


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — CONSULTA EXTERNA ──────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/con/consultas', methods=['GET'])
@auth.login_required
def api_con_listar():
    return ok(con.listar_consultas(
        request.args.get('data'),
        request.args.get('estado'),
        request.args.get('especialidade')))

@app.route('/api/con/consultas', methods=['POST'])
@auth.login_required
def api_con_criar():
    d = request.get_json()
    if not d.get('nome'):          return erro('Campo obrigatório: Nome')
    if not d.get('especialidade'): return erro('Campo obrigatório: Especialidade')
    if not d.get('data_consulta'): return erro('Campo obrigatório: Data')
    return ok({'id': con.criar_consulta(d)}, 'Consulta criada com sucesso')

@app.route('/api/con/consultas/<cid>', methods=['PUT'])
@auth.login_required
def api_con_actualizar(cid):
    con.actualizar_consulta(cid, request.get_json())
    return ok(msg='Consulta actualizada com sucesso')

@app.route('/api/con/consultas/<cid>', methods=['DELETE'])
@auth.login_required
def api_con_del(cid):
    con.eliminar_consulta(cid)
    return ok(msg='Consulta eliminada com sucesso')

@app.route('/api/con/estatisticas', methods=['GET'])
@auth.login_required
def api_con_stats():
    data = request.args.get('data', hoje())
    return ok(con.estatisticas_con(data[:7]+'-01', data))


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — BLOCO OPERATÓRIO ──────────────────────────────────────════════════
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/bloco/cirurgias', methods=['GET'])
@auth.login_required
def api_bloco_listar():
    return ok(bloco.listar_cirurgias(
        request.args.get('data'),
        request.args.get('estado'),
        request.args.get('urgencia')))

@app.route('/api/bloco/cirurgias', methods=['POST'])
@auth.login_required
def api_bloco_criar():
    d = request.get_json()
    if not d.get('nome'):          return erro('Campo obrigatório: Nome')
    if not d.get('tipo_cirurgia'): return erro('Campo obrigatório: Tipo de cirurgia')
    if not d.get('cirurgiao'):     return erro('Campo obrigatório: Cirurgião')
    if not d.get('data_prog'):     return erro('Campo obrigatório: Data')
    return ok({'id': bloco.criar_cirurgia(d)}, 'Cirurgia criada com sucesso')

@app.route('/api/bloco/cirurgias/<bid>', methods=['PUT'])
@auth.login_required
def api_bloco_actualizar(bid):
    bloco.actualizar_cirurgia(bid, request.get_json())
    return ok(msg='Cirurgia actualizada com sucesso')

@app.route('/api/bloco/cirurgias/<bid>', methods=['DELETE'])
@auth.login_required
def api_bloco_del(bid):
    bloco.eliminar_cirurgia(bid)
    return ok(msg='Cirurgia eliminada com sucesso')

@app.route('/api/bloco/estatisticas', methods=['GET'])
@auth.login_required
def api_bloco_stats():
    data = request.args.get('data', hoje())
    return ok(bloco.estatisticas_bloco(data[:7]+'-01', data))


# ══════════════════════════════════════════════════════════════════════════════
# ─── API — FISIOTERAPIA ──────────────────────────────────────────────────────
# ══════════════════════════════════════════════════════════════════════════════

@app.route('/api/fisio/doentes', methods=['GET'])
@auth.login_required
def api_fisio_doentes():
    return ok(fisio.listar_doentes())

@app.route('/api/fisio/doentes', methods=['POST'])
@auth.login_required
def api_fisio_criar():
    d = request.get_json()
    if not d.get('nome'):        return erro('Campo obrigatório: Nome')
    if not d.get('diagnostico'): return erro('Campo obrigatório: Diagnóstico')
    if not d.get('data_entrada'):return erro('Campo obrigatório: Data de entrada')
    return ok({'id': fisio.criar_doente(d)}, 'Doente registado com sucesso')

@app.route('/api/fisio/doentes/<fid>', methods=['PUT'])
@auth.login_required
def api_fisio_actualizar(fid):
    fisio.actualizar_doente(fid, request.get_json())
    return ok(msg='Doente actualizado com sucesso')

@app.route('/api/fisio/doentes/<fid>', methods=['DELETE'])
@auth.login_required
def api_fisio_del(fid):
    fisio.desactivar_doente(fid)
    return ok(msg='Doente desactivado com sucesso')

@app.route('/api/fisio/sessoes', methods=['GET'])
@auth.login_required
def api_fisio_sessoes():
    return ok(fisio.listar_sessoes(
        request.args.get('doente_id'),
        request.args.get('inicio'), request.args.get('fim')))

@app.route('/api/fisio/sessoes', methods=['POST'])
@auth.login_required
def api_fisio_sessao():
    d = request.get_json()
    if not d.get('doente_id'):    return erro('Campo obrigatório: doente_id')
    if not d.get('tipo_terapia'): return erro('Campo obrigatório: Tipo de terapia')
    if not d.get('data_sessao'):  return erro('Campo obrigatório: Data')
    return ok({'id': fisio.registar_sessao(d)}, 'Sessão registada com sucesso')

@app.route('/api/fisio/sessoes/<sid>', methods=['DELETE'])
@auth.login_required
def api_fisio_sessao_del(sid):
    fisio.eliminar_sessao(sid)
    return ok(msg='Sessão eliminada com sucesso')

@app.route('/api/fisio/estatisticas', methods=['GET'])
@auth.login_required
def api_fisio_stats():
    data = request.args.get('data', hoje())
    return ok(fisio.estatisticas_fisio(data[:7]+'-01', data))


# ─── ARRANCAR ────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 55)
    print("  Hospital do Prenda — Sistema de Gestão")
    print("  Acede em: http://localhost:5000")
    print("  Login inicial: admin / admin123")
    print("=" * 55)
    app.run(debug=True, host='0.0.0.0', port=5000)
