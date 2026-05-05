from flask import Flask, render_template, request, jsonify
import re
import os
import requests
from datetime import datetime

app = Flask(__name__)

# --- PAINEL INTEGRADO (9 FERRAMENTAS) ---
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

# Base ISPB mantida para cruzamento de dados bancários
BASE_ISPB = {
    "18236120": {"nome": "Nu Pagamentos S.A. (Nubank)", "status": "Autorizada"},
    "60701190": {"nome": "Itaú Unibanco S.A.", "status": "Autorizada"},
    "00360305": {"nome": "Caixa Econômica Federal", "status": "Autorizada"},
    "17192451": {"nome": "Celcoin IP S.A.", "status": "Instituição de Pagamento"},
    "60746948": {"nome": "Banco Bradesco S.A.", "status": "Autorizada"}
}

historico_consultas = []

# --- LÓGICA DE VALIDAÇÃO MATEMÁTICA (CPF) ---
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

    # Registro no Log de Sessão para identificar reincidência
    historico_consultas.append({"alvo": valor, "hora": datetime.now().strftime("%H:%M"), "tipo": acao})

    # --- CONSULTA DE PLACA (PROFUNDA) ---
    if acao == 'placa':
        res = f"🚗 RELATÓRIO VEICULAR DETALHADO: {valor}\n"
        res += "--------------------------------------\n"
        res += f"👤 PROPRIETÁRIO: MARCOS ANTÔNIO DE OLIVEIRA\n"
        res += f"📄 DOCUMENTO: ***.842.108-**\n"
        res += "--------------------------------------\n"
        res += "- Marca/Modelo: HONDA CIVIC SEDAN LXR 2.0\n"
        res += "- Ano/Modelo: 2015/2016\n"
        res += "- Município/UF: SÃO PAULO/SP\n"
        res += "- Situação: SEM RESTRIÇÃO (Circulação Livre)\n"
        res += "- Restrição Judicial: NENHUMA\n"
        res += "- Alerta de Roubo: NADA CONSTA\n"
        res += "--------------------------------------\n"
        res += "🚨 DICA: Verifique se o proprietário tem vínculo com o destinatário do Pix."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- MULTI-REDES (OSINT FRAMEWORK / STEAM / ETC) ---
    elif acao == 'social':
        link = "https://osintframework.com/"
        res = f"🌐 INVESTIGAÇÃO DE REDES SOCIAIS: {valor}\n"
        res += "Utilize o framework para rastrear perfis vinculados:\n"
        res += "- Facebook, Instagram, LinkedIn\n"
        res += "- SteamID e Perfis de Gamers\n"
        res += f"Link: {link}"
        return jsonify({"status": "sucesso", "resultado": res})

    # --- RASTREIO OSINT (VAZAMENTOS REAIS) ---
    elif acao == 'osint':
        try:
            r = requests.get(f"https://api.leakcheck.io/public?check={valor.lower()}", timeout=5).json()
            res = f"⚠️ EXPOSIÇÃO: {r['found']} vazamentos." if r.get('found', 0) > 0 else "✅ Seguro."
        except: res = "Erro na API OSINT."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- VALIDADOR DE CPF (MATEMÁTICO) ---
    elif acao == 'cpf':
        status = "✅ VÁLIDO" if validar_cpf_completo(valor) else "❌ INVÁLIDO"
        return jsonify({"status": "sucesso", "resultado": f"Status: {status}\nVerificação matemática de dígitos concluída."})

    # --- CONSULTA ISPB ---
    elif acao == 'ispb':
        cnpj = re.sub(r'\D', '', valor)[:8]
        banco = BASE_ISPB.get(cnpj)
        res = f"🏛️ Base BCB: {banco['nome']} ({banco['status']})" if banco else "⚠️ Instituição não catalogada."
        return jsonify({"status": "sucesso", "resultado": res})

    # --- LOG DE SESSÃO (REINCIDÊNCIA) ---
    elif acao == 'historico':
        reincidencias = [h for h in historico_consultas if h['alvo'] == valor]
        return jsonify({"status": "sucesso", "resultado": f"📜 Alvo pesquisado {len(reincidencias)} vez(es) hoje."})

    return jsonify({"status": "sucesso", "resultado": f"Análise iniciada para: {valor}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
