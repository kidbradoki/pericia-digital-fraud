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
    except Exception: return {}

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
    if not valor: return jsonify({"status": "erro", "mensagem": "Insira um alvo."})

    historico_consultas.append({"alvo": valor, "tipo": acao, "hora": datetime.now().strftime("%H:%M:%S")})

    # --- 1. CONSULTA CNPJ (GRATUITA - RECEITA WS) ---
    if acao == 'cpf' and len(re.sub(r'\D', '', valor)) > 11:
        cnpj = re.sub(r'\D', '', valor)
        try:
            r = requests.get(f"https://receitaws.com.br/v1/cnpj/{cnpj}", timeout=5).json()
            if r.get('status') == 'OK':
                cont = f" 🏢 RAZÃO: {r.get('nome')}\n 🆔 CNPJ:  {valor}\n 📅 INÍCIO: {r.get('abertura')}\n"
                cont += f" 📍 CIDADE: {r.get('municipio')}-{r.get('uf')}\n 📞 FONE:   {r.get('telefone')}\n"
                cont += f" 📧 EMAIL:  {r.get('email')}\n 💰 CAPITAL: R$ {r.get('capital_social')}"
                return jsonify({"status": "sucesso", "resultado": gerar_moldura("CNPJ FEDERAL (OPEN-DATA)", cont)})
        except: pass

    # --- 2. TELEFONE (GRATUITO - REDES E HLR) ---
    elif acao == 'social' and any(c.isdigit() for c in valor):
        num = re.sub(r'\D', '', valor)
        cont = f" 📞 NÚMERO: {valor}\n 📡 TIPO: Móvel/WhatsApp\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🛠️ LINKS DE INVESTIGAÇÃO DIRETA:\n"
        cont += f" 🔗 WHATSAPP: https://wa.me/{num}\n"
        cont += f" 🔗 SYNC.ME:  https://sync.me/search?number={num}\n"
        cont += f" 🔗 TRUECALLER: https://www.truecaller.com/search/br/{num}\n"
        cont += " 💡 DICA: O Sync.me costuma revelar o nome real."
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("INTELIGÊNCIA DE TELEFONE", cont)})

    # --- 3. OSINT (GRATUITO - DORKS E VAZAMENTOS) ---
    elif acao == 'osint':
        valor_osint = valor.lower()
        cont = f" 🎯 ALVO: {valor_osint}\n 📡 VARREDURA: Bases Públicas\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 📂 COMANDOS AVANÇADOS (DORKS):\n"
        cont += f" 🔍 NO GOOGLE: \"{valor_osint}\"\n"
        cont += f" 🔍 EM DOCUMENTOS: \"{valor_osint}\" filetype:pdf\n"
        cont += f" 🔍 EM LISTAS: \"{valor_osint}\" filetype:xlsx\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔗 VER VAZAMENTOS: https://leakcheck.io/\n"
        cont += " 🔗 REDES SOCIAIS: https://knowem.com/"
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("DOSSIÊ DE FONTES ABERTAS", cont)})

    # --- 4. CONSULTA PLACA (BASE LOCAL) ---
    elif acao == 'placa':
        base = carregar_base_veiculos()
        p = valor.replace("-", "").replace(" ", "")
        v = base.get(p)
        if v:
            cont = f" 📂 ALVO: {p}\n 👤 NOME: {v['proprietario']}\n 🆔 DOC:  {v['documento']}\n"
            cont += "──────────────────────────────────────────\n"
            cont += f" 🚘 CARRO: {v['modelo']}\n 📅 ANO:   {v['ano']}\n 📍 LOCAL: {v['cidade']}\n"
            cont += f" 🚨 ALERTA: {v['alerta']}"
            return jsonify({"status": "sucesso", "resultado": gerar_moldura("RELATÓRIO VEICULAR", cont)})
        return jsonify({"status": "sucesso", "resultado": "❌ NADA CONSTA NA BASE LOCAL."})

    # --- 5. VALIDADOR DE CPF ---
    elif acao == 'cpf':
        validade = "✅ VÁLIDO" if len(valor) == 11 else "❌ FORMATO INVÁLIDO"
        cont = f" 👤 CPF: {valor}\n ⚖️ STATUS: {validade}\n"
        cont += "──────────────────────────────────────────\n"
        cont += " 🔎 BUSCAR NO GOOGLE: \n"
        cont += f" 🔗 https://www.google.com/search?q=\"{valor}\""
        return jsonify({"status": "sucesso", "resultado": gerar_moldura("PERÍCIA DE CPF", cont)})

    return jsonify({"status": "sucesso", "resultado": "Ferramenta em modo de escuta..."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
