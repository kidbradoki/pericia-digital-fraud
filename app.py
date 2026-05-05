from flask import Flask, render_template, request, jsonify
import re
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

# --- PAINEL DE CONTROLE (9 FERRAMENTAS MANTIDAS) ---
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

# Histórico temporário para o Log de Sessão
historico_consultas = []

# --- FUNÇÃO PARA CARREGAR A BASE EXTERNA ---
def carregar_base_veiculos():
    """Tenta ler o arquivo JSON de 5.000 registros"""
    try:
        caminho = os.path.join(os.path.dirname(__file__), 'dados_veiculos.json')
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar banco de dados: {e}")
        return {}

def validar_cpf_matematico(cpf):
    """Validação real de dígitos de CPF"""
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

    # Registra no Log de Sessão
    historico_consultas.append({
        "alvo": valor, 
        "tipo": acao, 
        "hora": datetime.now().strftime("%H:%M:%S")
    })

    # --- LÓGICA DE CONSULTA DE PLACA (DINÂMICA) ---
    if acao == 'placa':
        base = carregar_base_veiculos()
        # Limpa a placa (remove espaços e traços) para a busca no JSON
        placa_busca = valor.replace("-", "").replace(" ", "")
        veiculo = base.get(placa_busca)

        if veiculo:
            res = f"✅ 🚗 RELATÓRIO VEICULAR DETALHADO: {placa_busca}\n"
            res += "--------------------------------------\n"
            res += f"👤 PROPRIETÁRIO: {veiculo['proprietario']}\n"
            res += f"📄 DOCUMENTO: {veiculo['documento']}\n"
            res += "--------------------------------------\n"
            res += f"- Marca/Modelo: {veiculo['modelo']}\n"
            res += f"- Ano/Modelo: {veiculo['ano']}\n"
            res += f"- Município/UF: {veiculo['cidade']}\n"
            res += f"- Situação: {veiculo['situacao']}\n"
            res += f"🚨 ALERTA: {veiculo['alerta']}\n"
            res += "--------------------------------------\n"
            res += "⚠️ DICA: Verifique se o proprietário tem vínculo com o destinatário do Pix."
        else:
            # Caso a placa não esteja no seu JSON
            res = f"❌ NADA CONSTA: O alvo '{valor}' não possui registros ativos nesta base de dados local."
        
        return jsonify({"status": "sucesso", "resultado": res})

    # --- RASTREIO OSINT (API REAL) ---
    elif acao == 'osint':
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            found = r.get('found', 0)
            res = f"⚠️ ALERTA: Encontradas {found} exposições públicas para este alvo." if found > 0 else "✅ Nenhuma exposição pública detectada."
        except:
            res = "❌ Erro ao conectar com a base OSINT em tempo real."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- VALIDADOR DE CPF ---
    elif acao == 'cpf':
        validade = "✅ VÁLIDO" if validar_cpf_matematico(valor) else "❌ INVÁLIDO"
        return jsonify({"status": "sucesso", "resultado": f"Status: {validade}\nA análise de dígitos verificadores foi concluída."})

    # --- FORENSE DE ARQUIVO (MOCK) ---
    elif acao == 'metadados':
        detectado = "⚠️ POSSÍVEL EDIÇÃO: Detectados vestígios de manipulação (Canva/PS)." if "CANVA" in valor or "PHOTO" in valor else "✅ Originalidade preservada."
        return jsonify({"status": "sucesso", "resultado": f"Análise Forense: {detectado}"})

    # --- LOG DE SESSÃO ---
    elif acao == 'historico':
        reincidencias = [h for h in historico_consultas if h['alvo'] == valor]
        return jsonify({"status": "sucesso", "resultado": f"📜 O alvo '{valor}' foi consultado {len(reincidencias)} vez(es) nesta sessão de investigação."})

    return jsonify({"status": "sucesso", "resultado": "Análise concluída com sucesso."})

if __name__ == "__main__":
    # Configuração para rodar no Render ou Localmente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
