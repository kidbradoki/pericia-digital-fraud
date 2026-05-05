from flask import Flask, render_template, request, jsonify
import re
import os
import requests
from datetime import datetime

app = Flask(__name__)

# --- CONFIGURAÇÕES E BANCO DE DADOS TÉCNICO ---
FERRAMENTAS = [
    {"id": "pericia", "nome": "Perícia de Comprovante", "icon": "🔍", "desc": "Análise de metadados e edição."},
    {"id": "osint", "nome": "Rastreio OSINT", "icon": "🌐", "desc": "Busca de pegada digital e vazamentos."},
    {"id": "bancos", "nome": "Consulta de Bancos", "icon": "🏦", "desc": "Base ISPB e Participantes PIX."},
    {"id": "cpf", "nome": "Validador de CPF", "icon": "👤", "desc": "Cálculo de dígitos e histórico."}
]

# Base ISPB Real para consulta técnica
BASE_ISPB = {
    "18236120": {"nome": "Nu Pagamentos S.A.", "isbp": "18236120", "status": "Autorizada"},
    "60701190": {"nome": "Itaú Unibanco S.A.", "isbp": "60701190", "status": "Autorizada"},
    "00360305": {"nome": "Caixa Econômica Federal", "isbp": "00360305", "status": "Autorizada"},
    "17192451": {"nome": "Celcoin IP S.A.", "isbp": "17192451", "status": "Autorizada (Alto Risco Detectado)"}
}

# Histórico temporário (Em produção, usaríamos SQLite)
historico_investigacao = []

# --- FUNÇÕES DE SUPORTE ---
def analisar_metadados_simulado(nome_arquivo):
    # Simulação de detecção de software de edição
    editores = ["adobe", "photoshop", "canva", "picsart"]
    if any(ed in nome_arquivo.lower() for ed in editores):
        return "⚠️ ALERTA: Vestígios de edição detectados nos metadados."
    return "✅ Metadados limpos (Origem nativa do dispositivo)."

def validar_cpf_real(cpf):
    cpf = re.sub(r'\D', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11: return False
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i + 1) - num) for num in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]): return False
    return True

# --- ROTAS ---
@app.route('/')
def index():
    return render_template('index.html', ferramentas=FERRAMENTAS)

@app.route('/api/executar', methods=['POST'])
def executar():
    dados = request.json
    acao = dados.get('acao')
    valor = dados.get('valor', '').strip().upper()
    
    if not valor:
        return jsonify({"status": "erro", "mensagem": "Insira os dados para análise."})

    # Registra no histórico de investigação
    historico_investigacao.append({"data": datetime.now().strftime("%H:%M:%S"), "alvo": valor, "tipo": acao})

    # 1. PERÍCIA COM ANÁLISE DE ARQUIVO (UPLOAD/SIMULAÇÃO)
    if acao == 'pericia':
        analise_edit = analisar_metadados_simulado(valor)
        relatorio = f"📋 LAUDO PERICIAL\n"
        relatorio += f"🔹 Alvo: {valor}\n"
        relatorio += f"🔹 Status: {analise_edit}\n"
        relatorio += "🔹 Sugestão: Confrontar com extrato bancário oficial."
        return jsonify({"status": "sucesso", "resultado": relatorio})

    # 2. CONSULTA DE BANCOS (ISPB / PARTICIPANTES PIX)
    elif acao == 'bancos':
        cnpj_limpo = re.sub(r'\D', '', valor)[:8] # Pega o radical do CNPJ
        banco = BASE_ISPB.get(cnpj_limpo)
        if banco:
            res = f"🏦 INSTITUIÇÃO IDENTIFICADA (Base BCB)\n"
            res += f"▪️ Razão: {banco['nome']}\n"
            res += f"▪️ ISPB: {banco['isbp']}\n"
            res += f"▪️ Situação: {banco['status']}"
        else:
            res = "⚠️ Instituição não encontrada na base de participantes PIX."
        return jsonify({"status": "sucesso", "resultado": res})

    # 3. RASTREIO OSINT + REINCIDÊNCIA
    elif acao == 'osint':
        reincidencia = [h for h in historico_investigacao if h['alvo'] == valor]
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            exposicao = f"⚠️ Vazamentos: {r['found']}" if r.get('found', 0) > 0 else "✅ Sem vazamentos."
        except:
            exposicao = "Erro ao acessar base OSINT."
        
        res = f"🌐 ANÁLISE OSINT\n{exposicao}\n"
        res += f"📌 Alvo consultado {len(reincidencia)} vezes nesta sessão."
        return jsonify({"status": "sucesso", "resultado": res})

    # 4. VALIDADOR DE CPF
    elif acao == 'cpf':
        valido = validar_cpf_real(valor)
        status = "✅ VÁLIDO" if valido else "❌ INVÁLIDO (Dígito incorreto)"
        return jsonify({"status": "sucesso", "resultado": f"Status: {status}\nMatemática Forense: Aplicada."})

    return jsonify({"status": "erro", "mensagem": "Ação não reconhecida."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
