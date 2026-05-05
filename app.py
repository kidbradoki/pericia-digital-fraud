from flask import Flask, render_template, request, jsonify
import re
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# --- PAINEL DE CONTROLE (9 FERRAMENTAS) ---
FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia Visual", "icon": "🔍", "desc": "Layout e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Vazamentos e pegada digital."},
    {"id": "bancos", "nome": "Vínculos Bancários", "icon": "🏦", "desc": "Busca de contas por CPF."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo e região fiscal."},
    {"id": "metadados", "nome": "Forense de Arquivo", "icon": "📁", "desc": "Análise de edição (Canva/PS)."},
    {"id": "ispb", "nome": "Consulta ISPB", "icon": "🏛️", "desc": "Base oficial Banco Central."},
    {"id": "social", "nome": "Multi-Redes", "icon": "📱", "desc": "Investigar perfis (FB, Steam, etc)."},
    {"id": "placa", "nome": "Consulta Placa", "icon": "🚗", "desc": "Dados e Nome do Proprietário."},
    {"id": "historico", "nome": "Log de Sessão", "icon": "📜", "desc": "Reincidência de alvos."}
]

historico_consultas = []

def carregar_base_veiculos():
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'dados_veiculos.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def validar_cpf_matematico(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
    return True

@app.route('/')
def index():
    return render_template('index.html', ferramentas=FERRAMENTAS)

@app.route('/api/executar', methods=['POST'])
def executar():
    dados = request.json
    acao = dados.get('acao')
    valor = dados.get('valor', '').strip().upper()
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Insira um alvo para análise."})

    historico_consultas.append({"alvo": valor, "tipo": acao, "hora": datetime.now().strftime("%H:%M:%S")})

    # --- CONSULTA DE PLACA (VISUAL FORENSE) ---
    if acao == 'placa':
        base = carregar_base_veiculos()
        placa_busca = valor.replace("-", "").replace(" ", "")
        veiculo = base.get(placa_busca)

        if veiculo:
            res =  "╔════════════════════════════════════════╗\n"
            res += "║       RELATÓRIO DE INTELIGÊNCIA        ║\n"
            res += "╚════════════════════════════════════════╝\n"
            res += f" 📂 ALVO: {placa_busca}\n"
            res += f" 👤 NOME: {veiculo['proprietario']}\n"
            res += f" 🆔 DOC:  {veiculo['documento']}\n"
            res += "──────────────────────────────────────────\n"
            res += f" 🚘 VEÍCULO: {veiculo['modelo']}\n"
            res += f" 📅 ANO:     {veiculo['ano']}\n"
            res += f" 📍 LOCAL:   {veiculo['cidade']}\n"
            res += "──────────────────────────────────────────\n"
            status_icon = "🟢" if "SEM RESTRIÇÃO" in veiculo['situacao'] else "🔴"
            res += f" {status_icon} STATUS:  {veiculo['situacao']}\n"
            res += f" 📌 ALERTA:  {veiculo['alerta']}\n"
            res += "──────────────────────────────────────────\n"
            res += f" 🕒 CONSULTA EM: {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        else:
            res = f"❌ NADA CONSTA: O alvo '{valor}' não possui registros ativos nesta base de dados local."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- RASTREIO OSINT (BUSCA AMPLIADA) ---
    elif acao == 'osint':
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            found = r.get('found', 0)
            
            res =  "🌐 [ VARREDURA OSINT EM ANDAMENTO ]\n"
            res += "──────────────────────────────────\n"
            if found > 0:
                res += f"⚠️ ALERTA CRÍTICO: {found} VAZAMENTOS!\n"
                res += f"O termo '{valor}' foi exposto em bancos de dados.\n"
                res += "Sugestão: Verifique 'Have I Been Pwned' para detalhes."
            else:
                res += "✅ TERMO LIMPO: Nenhuma exposição pública imediata.\n"
            
            res += "\n🔍 PEGADA DIGITAL (SUGESTÕES):\n"
            res += f"- Sherlock: Analisar user '{valor}' em 300+ redes.\n"
            res += f"- Maigret: Buscar dossiê completo de '{valor}'."
        except:
            res = "❌ ERRO: Falha na conexão com os servidores OSINT."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- VALIDADOR DE CPF ---
    elif acao == 'cpf':
        validade = "✅ VÁLIDO" if validar_cpf_matematico(valor) else "❌ INVÁLIDO"
        res =  "👤 [ VALIDADOR FISCAL ]\n"
        res += "──────────────────────\n"
        res += f"ALVO: {valor}\n"
        res += f"STATUS: {validade}\n"
        res += "Cálculo de dígitos concluído."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- LOG DE SESSÃO ---
    elif acao == 'historico':
        reincidencias = [h for h in historico_consultas if h['alvo'] == valor]
        res =  "📜 [ HISTÓRICO DE INVESTIGAÇÃO ]\n"
        res += "──────────────────────────────\n"
        res += f"Alvo: {valor}\n"
        res += f"Consultas: {len(reincidencias)} vez(es) nesta sessão."
        return jsonify({"status": "sucesso", "resultado": res})

    return jsonify({"status": "sucesso", "resultado": "Processando análise técnica..."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
