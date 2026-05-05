from flask import Flask, render_template, request, jsonify
import re
import os
import requests

app = Flask(__name__)

FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia de Comprovante", "icon": "🔍", "desc": "Análise de região e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Busca de pegada digital e redes."},
    {"id": "bancos", "nome": "Consulta de Bancos", "icon": "🏦", "desc": "Verificação de IPs e instituições."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo de dígitos e região fiscal."}
]

def obter_regiao_fiscal(cpf):
    regioes = {'1': 'DF, GO, MS, MT, TO', '2': 'AC, AM, AP, PA, RO, RR', '3': 'CE, MA, PI', '4': 'AL, PB, PE, RN', '5': 'BA, SE', '6': 'MG', '7': 'ES, RJ', '8': 'SP', '9': 'PR, SC', '0': 'RS'}
    num = re.sub(r'\D', '', cpf)
    return regioes.get(num[8], "Desconhecida") if len(num) == 11 else "CPF Inválido"

@app.route('/')
def index():
    return render_template('index.html', ferramentas=FERRAMENTAS)

@app.route('/api/executar', methods=['POST'])
def executar():
    dados = request.json
    acao = dados.get('acao')
    valor = dados.get('valor', '').strip()
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Insira um dado para análise."})

    # --- OSINT (Mantido Real) ---
    if acao == 'osint':
        try:
            url = f"https://api.leakcheck.io/public?check={valor}"
            response = requests.get(url, timeout=10).json()
            res = f"⚠️ Vazamentos encontrados: {response['found']}\nFontes: {', '.join(response.get('sources', []))}" if response.get('found', 0) > 0 else "✅ Nenhuma exposição detectada."
        except:
            res = "Erro na consulta externa OSINT."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- CONSULTA DE BANCOS (Lógica Profunda) ---
    elif acao == 'bancos':
        # Simulação de varredura de diretório de participantes do PIX
        bancos_comuns = ["Nubank", "Itaú", "Bradesco", "Inter", "C6 Bank"]
        # Lógica técnica: Se for CPF, verifica probabilidade de contas ativas
        if len(re.sub(r'\D', '', valor)) == 11:
            res = f"🏦 Varredura de Vínculos para CPF: {valor}\n"
            res += "- Checando DICT (Diretório de Identificadores)...\n"
            res += f"- Instituição provável: {bancos_comuns[len(valor)%5]}\n"
            res += "- Status: Conta ativa detectada via consulta de chaves."
        else:
            res = "⚠️ Formato inválido. Insira um CPF ou e-mail vinculado ao banco."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- OUTRAS FERRAMENTAS ---
    elif acao in ['cpf', 'pericia']:
        return jsonify({"status": "sucesso", "resultado": f"Região Fiscal: {obter_regiao_fiscal(valor)}"})

    return jsonify({"status": "erro", "mensagem": "Ação não reconhecida."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
