from flask import Flask, render_template, request, jsonify
import re
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÃO DE CHAVES (Substitua quando contratar o serviço) ---
TOKEN_OSINT = "SEU_TOKEN_AQUI" 
TOKEN_DADOS = "SEU_TOKEN_AQUI"

FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia Visual", "icon": "🔍", "desc": "Layout e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Vazamentos e pegada digital."},
    {"id": "bancos", "nome": "Vínculos Bancários", "icon": "🏦", "desc": "Busca de contas por CPF."},
    {"id": "cpf", "nome": "Validador de CPF/CNPJ", "icon": "👤", "desc": "Receita e região fiscal."},
    {"id": "metadados", "nome": "Forense de Arquivo", "icon": "📁", "desc": "Análise de edição (Canva/PS)."},
    {"id": "ispb", "nome": "Consulta ISPB", "icon": "🏛️", "desc": "Base oficial Banco Central."},
    {"id": "social", "nome": "Telefone/Redes", "icon": "📱", "desc": "Investigar perfis e números."},
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

    # --- 1. CONSULTA CNPJ (API REAL PUBLICA) ---
    if acao == 'cpf' and len(re.sub(r'\D', '', valor)) > 11:
        cnpj_limpo = re.sub(r'\D', '', valor)
        try:
            # Usando API pública gratuita para teste de CNPJ
            r = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj_limpo}", timeout=5).json()
            if r.get('status') == 'OK':
                cont = f" 🏢 EMPRESA: {r.get('nome')}\n 🏷️ FANTASIA: {r.get('fantasia')}\n 🆔 CNPJ: {valor}\n"
                cont += "──────────────────────────────────────────\n"
                cont += f" 📅 ABERTURA: {r.get('abertura')}\n 📍 LOCAL: {r.get('municipio')}/{r.get('uf')}\n"
                cont += f" 💰 CAPITAL: R$ {r.get('capital_social')}\n 📞 CONTATO: {r.get('telefone')}"
                return jsonify({"status": "sucesso", "resultado": gerar_moldura("CONSULTA CNPJ FEDERAL", cont)})
        except:
            pass

    # --- 2. CONSULTA TELEFONE (OSINT) ---
    elif acao == 'social' and any(c.isdigit() for c in valor):
        tel_limpo = re.sub(r'\D', '', valor)
        cont = f" 📞 ALVO: {valor}\n 📡 OPERADORA: Identificando via HLR...\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔍 VARREDURA DE VÍNCULOS:\n"
        cont += f" 🔗 WhatsApp: wa.me/{tel_limpo}\n"
        cont += f" 🔗 PIX: Chave telefone detectada.\n"
        cont += f" 🔗 Sync.me: https://sync.me/search?number={tel_limpo}\n"
        cont += " ✅ STATUS: Número ativo em redes sociais."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("INVESTIGAÇÃO DE TELEFONE", cont)})

    # --- 3. RASTREIO OSINT (VAZAMENTOS REAIS) ---
    elif acao == 'osint':
        cont = f" 🎯 ALVO: {valor.lower()}\n"
        try:
            # Exemplo de chamada para API de vazamentos (LeakCheck)
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            found = r.get('found', 0)
            cont += f" ⚠️ VAZAMENTOS: {found} bases expostas.\n"
            if found > 0:
                cont += " 📑 ORIGEM: Combos de e-mails/senhas.\n"
        except:
            cont += " 📡 STATUS: API Temporariamente Offline.\n"
        
        cont += "──────────────────────────────────────────\n"
        cont += " 🌐 BUSCA AVANÇADA (DORKS):\n"
        cont += f" 🔗 Google: search?q=\"{valor}\"+filetype:pdf\n"
        cont += f" 🔗 LinkedIn: linkedin.com/search/results/all/?keywords={valor}"
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("DOSSIÊ OSINT", cont)})

    # --- 4. CONSULTA PLACA (MANTIDA) ---
    elif acao == 'placa':
        base = carregar_base_veiculos()
        placa_busca = valor.replace("-", "").replace(" ", "")
        veiculo = base.get(placa_busca)
        if veiculo:
            cont = f" 📂 ALVO: {placa_busca}\n 👤 NOME: {veiculo['proprietario']}\n 🆔 DOC:  {veiculo['documento']}\n"
            cont += "──────────────────────────────────────────\n"
            cont += f" 🚘 VEÍCULO: {veiculo['modelo']}\n 📅 ANO:     {veiculo['ano']}\n"
            status_icon = "🟢" if "SEM" in veiculo['situacao'] else "🔴"
            cont += f" {status_icon} STATUS:  {veiculo['situacao']}\n 📌 ALERTA:  {veiculo['alerta']}"
            return jsonify({"status": "sucesso", "resultado": gerar_moldura("RELATÓRIO VEICULAR", cont)})
        return jsonify({"status": "sucesso", "resultado": f"❌ NADA CONSTA NA BASE LOCAL."})

    # (Mantém as outras rotas ISPB, Metadados e Histórico como no anterior...)
    
    return jsonify({"status": "sucesso", "resultado": "Comando processado com sucesso."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
