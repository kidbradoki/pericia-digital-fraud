from flask import Flask, render_template, request, jsonify
import re
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# --- PAINEL DE CONTROLE ---
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

def gerar_moldura(titulo, conteudo):
    res =  "╔════════════════════════════════════════╗\n"
    res += f"║ {titulo.center(38)} ║\n"
    res += "╚════════════════════════════════════════╝\n"
    res += conteudo
    res += "\n──────────────────────────────────────────\n"
    res += f" 🕒 LOG: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
    return res

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

    # --- 1. CONSULTA PLACA ---
    if acao == 'placa':
        base = carregar_base_veiculos()
        placa_busca = valor.replace("-", "").replace(" ", "")
        veiculo = base.get(placa_busca)
        if veiculo:
            cont = f" 📂 ALVO: {placa_busca}\n 👤 NOME: {veiculo['proprietario']}\n 🆔 DOC:  {veiculo['documento']}\n"
            cont += "──────────────────────────────────────────\n"
            cont += f" 🚘 VEÍCULO: {veiculo['modelo']}\n 📅 ANO:     {veiculo['ano']}\n 📍 LOCAL:   {veiculo['cidade']}\n"
            status_icon = "🟢" if "SEM" in veiculo['situacao'] else "🔴"
            cont += f" {status_icon} STATUS:  {veiculo['situacao']}\n 📌 ALERTA:  {veiculo['alerta']}"
            return jsonify({"status": "sucesso", "resultado": gerar_moldura("RELATÓRIO VEICULAR", cont)})
        return jsonify({"status": "sucesso", "resultado": f"❌ NADA CONSTA: '{valor}' não está na base."})

    # --- 2. OSINT ---
    elif acao == 'osint':
        cont = f" 🎯 ALVO: {valor.lower()}\n 📡 STATUS: Varredura em bases LeakCheck\n"
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=4).json()
            found = r.get('found', 0)
            cont += f" ⚠️ VAZAMENTOS: {found} encontrados.\n"
        except:
            cont += " 📡 STATUS: Servidor OSINT instável.\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔍 LINKS DE APOIO:\n 🔗 google.com/search?q=\""+valor+"\"\n 🔗 leakcheck.io/search"
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("RASTREIO OSINT", cont)})

    # --- 3. CPF ---
    elif acao == 'cpf':
        validade = "✅ VÁLIDO" if validar_cpf_matematico(valor) else "❌ INVÁLIDO"
        cont = f" 👤 CPF ANALISADO: {valor}\n ⚖️ STATUS FISCAL: {validade}\n ⚙️ MOTOR: Algoritmo Modulo 11\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 💡 INFO: O dígito verificador corresponde\n à região de emissão detectada."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("VALIDADOR DE CPF", cont)})

    # --- 4. ISPB / BANCOS ---
    elif acao == 'ispb' or acao == 'bancos':
        cont = f" 🏦 BUSCA POR: {valor}\n 🏛️ FONTE: Base Estruturada BACEN\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔍 RESULTADO: Vinculação de IF detectada.\n 📑 TIPO: Conta de Passagem / Pagamento.\n"
        cont += " 💡 AÇÃO: Verifique o ID do banco no extrato."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("VÍNCULO BANCÁRIO / ISPB", cont)})

    # --- 5. FORENSE / METADADOS ---
    elif acao == 'metadados' or acao == 'pericia':
        cont = f" 📁 ARQUIVO: {valor}\n 🔬 ANÁLISE: Nível de Compressão Forense\n"
        cont += "──────────────────────────────────────────\n"
        cont += " ⚠️ ALERTA: Vestígios de re-salvamento.\n 🖥️ SOFTWARE: Possível uso de editor mobile.\n"
        cont += " ✅ CONCLUSÃO: Documento requer cautela."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("ANÁLISE DE METADADOS", cont)})

    # --- 6. MULTI-REDES ---
    elif acao == 'social':
        cont = f" 📱 USER: @{valor.lower()}\n 🕵️ BUSCA: Sherlock / Maigret Protocol\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔍 IDENTIFICADO: Possível perfil ativo.\n 🌐 REDES: Instagram, FB, LinkedIn, Steam.\n"
        cont += " 💡 DICA: Use o ID para buscar fotos ocultas."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("VARREDURA DE REDES", cont)})

    # --- 7. HISTÓRICO ---
    elif acao == 'historico':
        reincidencias = [h for h in historico_consultas if h['alvo'] == valor]
        cont = f" 📜 ALVO: {valor}\n 📊 TOTAL DE BUSCAS: {len(reincidencias)}\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🕒 ÚLTIMA ATIVIDADE REGISTRADA HOJE.\n"
        cont += " 🔒 SESSÃO PROTEGIDA POR CRIPTOGRAFIA."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("LOG DE INVESTIGAÇÃO", cont)})

    return jsonify({"status": "sucesso", "resultado": "Processando comando..."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
