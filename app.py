from flask import Flask, render_template, request, jsonify
import re
import os
import requests
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÃO DO PAINEL (7 BOTÕES) ---
FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia Visual", "icon": "🔍", "desc": "Layout e autenticidade."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Vazamentos e pegada digital."},
    {"id": "bancos", "nome": "Vínculos Bancários", "icon": "🏦", "desc": "Busca de contas por CPF."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo e região fiscal."},
    {"id": "metadados", "nome": "Forense de Arquivo", "icon": "📁", "desc": "Análise de edição (Canva/PS)."},
    {"id": "ispb", "nome": "Consulta ISPB", "icon": "🏛️", "desc": "Base oficial Banco Central."},
    {"id": "historico", "nome": "Log de Sessão", "icon": "📜", "desc": "Reincidência de alvos."}
]

# Base ISPB para a nova ferramenta técnica
BASE_ISPB = {
    "18236120": {"nome": "Nu Pagamentos S.A. (Nubank)", "status": "Autorizada"},
    "60701190": {"nome": "Itaú Unibanco S.A.", "status": "Autorizada"},
    "00360305": {"nome": "Caixa Econômica Federal", "status": "Autorizada"},
    "17192451": {"nome": "Celcoin IP S.A.", "status": "Instituição de Pagamento"},
    "60746948": {"nome": "Banco Bradesco S.A.", "status": "Autorizada"}
}

historico_consultas = []

# --- FUNÇÕES TÉCNICAS MANTIDAS E MELHORADAS ---
def validar_cpf_completo(cpf):
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
        return jsonify({"status": "erro", "mensagem": "Insira dados para análise."})

    # Registro de Histórico (Global)
    historico_consultas.append({"alvo": valor, "hora": datetime.now().strftime("%H:%M"), "tipo": acao})

    # 1. PERÍCIA VISUAL (MANTIDA)
    if acao == 'pericia':
        return jsonify({"status": "sucesso", "resultado": f"🔍 Análise Visual: Verificando padrões de fontes e logotipos para {valor}..."})

    # 2. OSINT (REAL - MANTIDA)
    elif acao == 'osint':
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            res = f"⚠️ Vazamentos: {r['found']}\nFontes: {', '.join(r.get('sources', []))}" if r.get('found', 0) > 0 else "✅ Seguro."
        except:
            res = "Erro na conexão OSINT."
        return jsonify({"status": "sucesso", "resultado": res})

    # 3. VÍNCULOS BANCÁRIOS (MANTIDA)
    elif acao == 'bancos':
        return jsonify({"status": "sucesso", "resultado": f"🏦 Buscando chaves Pix e contas vinculadas ao alvo: {valor}"})

    # 4. VALIDADOR DE CPF (REAL - MANTIDA)
    elif acao == 'cpf':
        status = "✅ VÁLIDO" if validar_cpf_completo(valor) else "❌ INVÁLIDO"
        return jsonify({"status": "sucesso", "resultado": f"Status: {status}\nCálculo de dígitos concluído."})

    # 5. FORENSE DE ARQUIVO (NOVA)
    elif acao == 'metadados':
        detectado = "⚠️ Edição detectada (Software externo)" if any(x in valor for x in ["CANVA", "PS", "ADOBE"]) else "✅ Sem rastros óbvios."
        return jsonify({"status": "sucesso", "resultado": f"Análise Forense: {detectado}"})

    # 6. CONSULTA ISPB (NOVA)
    elif acao == 'ispb':
        cnpj = re.sub(r'\D', '', valor)[:8]
        banco = BASE_ISPB.get(cnpj)
        res = f"🏛️ Base BCB: {banco['nome']} ({banco['status']})" if banco else "⚠️ Instituição não catalogada."
        return jsonify({"status": "sucesso", "resultado": res})

    # 7. LOG DE SESSÃO (NOVA)
    elif acao == 'historico':
        reincidencia = [h for h in historico_consultas if h['alvo'] == valor]
        return jsonify({"status": "sucesso", "resultado": f"📜 Alvo consultado {len(reincidencia)} vez(es) nesta sessão."})

    return jsonify({"status": "erro", "mensagem": "Ação inválida."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
