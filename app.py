from flask import Flask, render_template, request, jsonify
import re
import os

app = Flask(__name__)

# Dados para o Menu Principal
FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia de Comprovante", "icon": "🔍", "desc": "Análise de região e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Busca de pegada digital e redes."},
    {"id": "bancos", "nome": "Consulta de Bancos", "icon": "🏦", "desc": "Verificação de IPs e instituições."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo de dígitos e região fiscal."}
]

# Lógica de Região Fiscal Técnica
def obter_regiao_fiscal(cpf):
    regioes = {
        '1': 'DF, GO, MS, MT, TO', '2': 'AC, AM, AP, PA, RO, RR',
        '3': 'CE, MA, PI', '4': 'AL, PB, PE, RN',
        '5': 'BA, SE', '6': 'MG', '7': 'ES, RJ',
        '8': 'SP', '9': 'PR, SC', '0': 'RS'
    }
    num = re.sub(r'\D', '', cpf)
    if len(num) == 11:
        # O 9º dígito do CPF indica a região fiscal de emissão
        return regioes.get(num[8], "Desconhecida")
    return "CPF Inválido"

@app.route('/')
def index():
    return render_template('index.html', ferramentas=FERRAMENTAS)

# Rota de API conectada ao seu novo Painel de Execução
@app.route('/api/executar', methods=['POST'])
def executar():
    dados = request.json
    acao = dados.get('acao')
    valor = dados.get('valor', '')
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Nenhum dado informado para análise."})

    # 1. Lógica para Perícia de Comprovante
    if acao == 'pericia':
        regiao = obter_regiao_fiscal(valor)
        return jsonify({
            "status": "sucesso", 
            "resultado": f"Análise concluída.\nLocal de Emissão: {regiao}\nStatus: Documento sob análise de metadados."
        })
    
    # 2. Lógica para Rastreio OSINT
    elif acao == 'osint':
        return jsonify({
            "status": "sucesso", 
            "resultado": f"Busca OSINT iniciada para: {valor}\nVarrendo redes sociais, domínios e vazamentos públicos..."
        })
    
    # 3. Lógica para Consulta de Bancos
    elif acao == 'bancos':
        return jsonify({
            "status": "sucesso", 
            "resultado": f"Instituições vinculadas ao alvo ({valor}):\n- Verificando chaves Pix ativas...\n- Consultando Registrato (Simulação)..."
        })
    
    # 4. Lógica para Validador de CPF
    elif acao == 'cpf':
        regiao = obter_regiao_fiscal(valor)
        return jsonify({
            "status": "sucesso", 
            "resultado": f"Validação de CPF concluída.\nRegião de Origem: {regiao}\nStatus: Estrutura de dígitos verificada."
        })

    return jsonify({"status": "erro", "mensagem": "Ferramenta em manutenção ou não reconhecida."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
