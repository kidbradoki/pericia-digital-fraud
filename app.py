from flask import Flask, render_template, request, jsonify
import re
import os
import requests  # Nova biblioteca para consultas reais

app = Flask(__name__)

FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia de Comprovante", "icon": "🔍", "desc": "Análise de região e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Busca de pegada digital e redes."},
    {"id": "bancos", "nome": "Consulta de Bancos", "icon": "🏦", "desc": "Verificação de IPs e instituições."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo de dígitos e região fiscal."}
]

def obter_regiao_fiscal(cpf):
    regioes = {
        '1': 'DF, GO, MS, MT, TO', '2': 'AC, AM, AP, PA, RO, RR',
        '3': 'CE, MA, PI', '4': 'AL, PB, PE, RN',
        '5': 'BA, SE', '6': 'MG', '7': 'ES, RJ',
        '8': 'SP', '9': 'PR, SC', '0': 'RS'
    }
    num = re.sub(r'\D', '', cpf)
    if len(num) == 11:
        return regioes.get(num[8], "Desconhecida")
    return "CPF Inválido"

@app.route('/')
def index():
    return render_template('index.html', ferramentas=FERRAMENTAS)

@app.route('/api/executar', methods=['POST'])
def executar():
    dados = request.json
    acao = dados.get('acao')
    valor = dados.get('valor', '')
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado informado."})

    # --- FERRAMENTA 1: OSINT REAL ---
    if acao == 'osint':
        try:
            # Consulta uma API pública de vazamentos (LeakCheck)
            url = f"https://api.leakcheck.io/public?check={valor}"
            response = requests.get(url, timeout=10).json()
            
            if response.get('found', 0) > 0:
                fontes = ", ".join(response.get('sources', []))
                res = f"⚠️ ALERTA: Dados expostos em {response['found']} vazamentos!\nFontes: {fontes}"
            else:
                res = "✅ Nenhuma exposição pública detectada para este alvo."
        except Exception as e:
            res = f"Busca local iniciada: {valor}. (Erro na API externa)"
        
        return jsonify({"status": "sucesso", "resultado": res})

    # --- OUTRAS FERRAMENTAS (Ainda em simulação) ---
    elif acao == 'pericia' or acao == 'cpf':
        regiao = obter_regiao_fiscal(valor)
        return jsonify({"status": "sucesso", "resultado": f"Região Fiscal: {regiao}"})
    
    elif acao == 'bancos':
        return jsonify({"status": "sucesso", "resultado": f"Consultando vínculos bancários para: {valor}..."})

    return jsonify({"status": "erro", "mensagem": "Ação não reconhecida"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
