"""
app.py — Servidor Flask do Sistema de Gestão do Hospital do Prenda
Executa com:  python app.py
Acede em:     http://localhost:5000
"""

import os
import json
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, send_file
import database as db

# ─── CONFIGURAÇÃO DO FLASK ───────────────────────────────────────────────────

app = Flask(__name__)
app.secret_key = 'hprenda-2026-secret'   # necessário para sessões

# Cria a base de dados e tabelas ao iniciar
db.criar_tabelas()


# ─── UTILITÁRIOS ─────────────────────────────────────────────────────────────

def hoje():
    """Devolve a data de hoje no formato YYYY-MM-DD."""
    return date.today().isoformat()


def resposta_ok(dados=None, mensagem='Operação realizada com sucesso'):
    """Formata uma resposta JSON de sucesso."""
    return jsonify({'ok': True, 'mensagem': mensagem, 'dados': dados})


def resposta_erro(mensagem, codigo=400):
    """Formata uma resposta JSON de erro."""
    return jsonify({'ok': False, 'mensagem': mensagem}), codigo


# ─── PÁGINAS (HTML) ──────────────────────────────────────────────────────────

@app.route('/')
def pagina_inicio():
    """Página inicial — lista de serviços."""
    return render_template('index.html', hoje=hoje())


@app.route('/cirurgia')
def pagina_cirurgia():
    """Página do serviço de Cirurgia Geral."""
    data = request.args.get('data', hoje())
    hospitais = db.listar_hospitais()
    return render_template(
        'cirurgia/index.html',
        data=data,
        hoje=hoje(),
        hospitais=hospitais,
    )


# ─── API — CIRURGIA — DOENTES ────────────────────────────────────────────────
# Cada rota corresponde a uma acção:
#   GET  /api/cirurgia/doentes          → listar doentes
#   POST /api/cirurgia/doentes          → criar novo doente
#   PUT  /api/cirurgia/doentes/<id>     → actualizar doente
#   DELETE /api/cirurgia/doentes/<id>   → eliminar doente

@app.route('/api/cirurgia/doentes', methods=['GET'])
def api_listar_doentes():
    """
    Lista todos os doentes internados.
    Parâmetro opcional: ?data=YYYY-MM-DD
    """
    data = request.args.get('data')
    doentes = db.listar_doentes_internados(data)
    return resposta_ok(doentes)


@app.route('/api/cirurgia/doentes', methods=['POST'])
def api_criar_doente():
    """
    Cria um novo doente.
    Recebe JSON no corpo do pedido com: nome, sexo, nup, idade, diagnostico, data_entrada, hospital
    """
    dados = request.get_json()

    # Validação dos campos obrigatórios
    if not dados.get('nome'):
        return resposta_erro('Campo obrigatório: Nome')
    if not dados.get('sexo'):
        return resposta_erro('Campo obrigatório: Sexo')
    if not dados.get('nup'):
        return resposta_erro('Campo obrigatório: NUP')

    novo_id = db.criar_doente(dados)
    return resposta_ok({'id': novo_id}, 'Doente registado com sucesso')


@app.route('/api/cirurgia/doentes/<doente_id>', methods=['PUT'])
def api_actualizar_doente(doente_id):
    """Actualiza os dados de um doente existente."""
    dados = request.get_json()
    if not db.obter_doente(doente_id):
        return resposta_erro('Doente não encontrado', 404)
    db.actualizar_doente(doente_id, dados)
    return resposta_ok(mensagem='Doente actualizado com sucesso')


@app.route('/api/cirurgia/doentes/<doente_id>', methods=['DELETE'])
def api_eliminar_doente(doente_id):
    """Elimina um doente pelo ID."""
    if not db.obter_doente(doente_id):
        return resposta_erro('Doente não encontrado', 404)
    db.eliminar_doente(doente_id)
    return resposta_ok(mensagem='Doente eliminado com sucesso')


# ─── API — CIRURGIA — ALTAS ──────────────────────────────────────────────────

@app.route('/api/cirurgia/altas', methods=['GET'])
def api_listar_altas():
    """Lista todas as altas. Parâmetros: ?inicio=YYYY-MM-DD&fim=YYYY-MM-DD"""
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    altas = db.listar_altas(inicio, fim)
    return resposta_ok(altas)


@app.route('/api/cirurgia/altas', methods=['POST'])
def api_registar_alta():
    """
    Regista a alta de um doente.
    Recebe JSON: { doente_id, diag_fim, data_saida, modo_saida }
    """
    dados = request.get_json()
    doente_id = dados.get('doente_id')

    if not doente_id:
        return resposta_erro('Campo obrigatório: doente_id')
    if not dados.get('data_saida'):
        return resposta_erro('Campo obrigatório: data_saida')
    if not dados.get('diag_fim'):
        return resposta_erro('Campo obrigatório: diagnóstico final')

    try:
        novo_id = db.registar_alta(doente_id, dados)
        return resposta_ok({'id': novo_id}, 'Alta registada com sucesso')
    except ValueError as e:
        return resposta_erro(str(e), 404)


@app.route('/api/cirurgia/altas/<alta_id>', methods=['DELETE'])
def api_eliminar_alta(alta_id):
    """Elimina um registo de alta."""
    db.eliminar_alta(alta_id)
    return resposta_ok(mensagem='Alta eliminada com sucesso')


# ─── API — CIRURGIA — ÓBITOS ─────────────────────────────────────────────────

@app.route('/api/cirurgia/obitos', methods=['GET'])
def api_listar_obitos():
    """Lista todos os óbitos. Parâmetros: ?inicio=YYYY-MM-DD&fim=YYYY-MM-DD"""
    inicio = request.args.get('inicio')
    fim = request.args.get('fim')
    obitos = db.listar_obitos(inicio, fim)
    return resposta_ok(obitos)


@app.route('/api/cirurgia/obitos', methods=['POST'])
def api_registar_obito():
    """
    Regista um óbito.
    Recebe JSON: { nome, sexo, nup, idade, diagnostico, diag_fim, data_entrada, data_obito, hospital }
    """
    dados = request.get_json()

    if not dados.get('nome'):
        return resposta_erro('Campo obrigatório: Nome')
    if not dados.get('data_obito'):
        return resposta_erro('Campo obrigatório: Data do óbito')

    novo_id = db.registar_obito(dados)
    return resposta_ok({'id': novo_id}, 'Óbito registado com sucesso')


@app.route('/api/cirurgia/obitos/<obito_id>', methods=['DELETE'])
def api_eliminar_obito(obito_id):
    """Elimina um registo de óbito."""
    db.eliminar_obito(obito_id)
    return resposta_ok(mensagem='Óbito eliminado com sucesso')


# ─── API — CIRURGIA — CAMAS ──────────────────────────────────────────────────

@app.route('/api/cirurgia/camas', methods=['GET'])
def api_obter_camas():
    """Devolve o número de camas para uma data. Parâmetro: ?data=YYYY-MM-DD"""
    data = request.args.get('data', hoje())
    camas = db.obter_camas(data)
    return resposta_ok({'data': data, 'camas': camas})


@app.route('/api/cirurgia/camas', methods=['POST'])
def api_guardar_camas():
    """Guarda o número de camas para uma data. Recebe JSON: { data, camas }"""
    dados = request.get_json()
    data = dados.get('data', hoje())
    camas = dados.get('camas', 0)

    if not isinstance(camas, int) or camas < 0:
        return resposta_erro('Número de camas inválido')

    db.guardar_camas(data, camas)
    return resposta_ok(mensagem=f'Camas guardadas: {camas} para {data}')


# ─── API — ESTATÍSTICAS ──────────────────────────────────────────────────────

@app.route('/api/cirurgia/estatisticas', methods=['GET'])
def api_estatisticas():
    """
    Devolve estatísticas calculadas para um período.
    Parâmetros: ?inicio=YYYY-MM-DD&fim=YYYY-MM-DD
    """
    data = request.args.get('data', hoje())
    inicio = request.args.get('inicio', data[:7] + '-01')  # primeiro dia do mês
    fim = request.args.get('fim', data)

    doentes_internados = db.listar_doentes_internados(data)
    altas = db.listar_altas(inicio, fim)
    obitos = db.listar_obitos(inicio, fim)
    camas = db.obter_camas(data)

    total_internados = len(doentes_internados)
    total_altas = len(altas)
    total_obitos = len(obitos)

    # Taxa de mortalidade (em percentagem)
    total_saidas = total_altas + total_obitos
    taxa_mortalidade = round((total_obitos / total_saidas * 100), 1) if total_saidas > 0 else 0

    # Dias de doente = soma dos dias internados
    dias_doente = 0
    for d in doentes_internados:
        try:
            entrada = datetime.strptime(d['data_entrada'], '%Y-%m-%d').date()
            dias_doente += (date.today() - entrada).days
        except Exception:
            pass

    return resposta_ok({
        'data': data,
        'internados': total_internados,
        'altas': total_altas,
        'obitos': total_obitos,
        'camas': camas,
        'taxa_mortalidade': taxa_mortalidade,
        'dias_doente': dias_doente,
    })


# ─── API — EXPORTAR / IMPORTAR JSON ─────────────────────────────────────────

@app.route('/api/cirurgia/exportar', methods=['GET'])
def api_exportar():
    """Exporta todos os dados da Cirurgia para JSON."""
    dados = db.exportar_json('cirurgia')
    nome_ficheiro = f"backup_cirurgia_{hoje()}.json"
    caminho = os.path.join(os.path.dirname(__file__), 'exports', nome_ficheiro)

    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    return send_file(caminho, as_attachment=True, download_name=nome_ficheiro)


@app.route('/api/cirurgia/importar', methods=['POST'])
def api_importar():
    """Importa dados de um ficheiro JSON enviado pelo browser."""
    if 'ficheiro' not in request.files:
        return resposta_erro('Nenhum ficheiro enviado')

    ficheiro = request.files['ficheiro']
    try:
        dados = json.load(ficheiro)
        db.importar_json(dados)
        return resposta_ok(mensagem='Dados importados com sucesso')
    except json.JSONDecodeError:
        return resposta_erro('Ficheiro JSON inválido')
    except Exception as e:
        return resposta_erro(f'Erro ao importar: {str(e)}')


# ─── ARRANCAR O SERVIDOR ─────────────────────────────────────────────────────

if __name__ == '__main__':
    print("=" * 55)
    print("  Hospital do Prenda — Sistema de Gestão")
    print("  Acede em: http://localhost:5000")
    print("=" * 55)
    # debug=True → recarrega automaticamente ao alterar o código
    app.run(debug=True, host='0.0.0.0', port=5000)
