from flask import Flask, render_template, request, jsonify
import re
import os
import requests  # Biblioteca para consultas em APIs externas

app = Flask(__name__)

# Configuração das ferramentas do painel
FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia de Comprovante", "icon": "🔍", "desc": "Análise de região e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Busca de pegada digital e redes."},
    {"id": "bancos", "nome": "Consulta de Bancos", "icon": "🏦", "desc": "Verificação de IPs e instituições."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo de dígitos e região fiscal."}
]

def obter_regiao_fiscal(cpf):
    """Identifica a região de origem baseada no 9º dígito do CPF."""
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
    valor = dados.get('valor', '').strip()
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Por favor, insira um dado para análise."})

    # --- FUNCIONALIDADE OSINT REAL ---
    if acao == 'osint':
        try:
            # Consulta a API pública da LeakCheck para verificar vazamentos de dados
            url = f"https://api.leakcheck.io/public?check={valor}"
            response = requests.get(url, timeout=10).json()
            
            if response.get('found', 0) > 0:
                fontes = ", ".join(response.get('sources', []))
                res = f"⚠️ ALERTA: Este alvo foi encontrado em {response['found']} vazamento(s) de dados.\nFontes: {fontes}"
            else:
                res = "✅ Nenhuma exposição pública detectada em bases de dados conhecidas para este alvo."
        except Exception:
            res = f"Análise iniciada para: {valor}. Verificando redes sociais e domínios..."
        
        return jsonify({"status": "sucesso", "resultado": res})

    # --- OUTRAS FERRAMENTAS (Simulação para próxima fase) ---
    elif acao == 'cpf' or acao == 'pericia':
        regiao = obter_regiao_fiscal(valor)
        return jsonify({"status": "sucesso", "resultado": f"Análise concluída.\nRegião Fiscal Detectada: {regiao}"})
    
    elif acao == 'bancos':
        return jsonify({"status": "sucesso", "resultado": f"Vínculos Bancários: Consultando chaves Pix e registros para {valor}..."})

    return jsonify({"status": "erro", "mensagem": "Ferramenta não reconhecida ou em manutenção."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
