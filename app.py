import os, re, pypdf, easyocr, requests
import numpy as np
from flask import Flask, render_template_string, request, redirect
from urllib.parse import urlparse

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializa o OCR
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GHOST INTEL v7.0</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; padding: 10px; text-align: center; }
        .flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; width: 100%; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background: #161b22; text-align: left; width: 48%; margin-bottom: 10px; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px 2px; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.65rem; text-transform: uppercase; text-decoration: none; border: none; cursor: pointer; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; } .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; } .btn-red { background-color: #da3633; } .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        h2 { color: #3fb950; font-size: 1rem; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 1px; }
        h3 { color: #8b949e; font-size: 0.55rem; border-bottom: 1px solid #30363d; padding-bottom: 3px; text-transform: uppercase; margin-bottom: 5px; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 8px; border-radius: 4px; font-size: 0.7rem; margin-top: 5px; }
        .status-badge { margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; text-align: center; }
        .fraude { background: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .real { background: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
        .dados-container { background: #000; color: #8b949e; font-family: monospace; font-size: 0.55rem; padding: 10px; margin-top: 8px; border-radius: 4px; border: 1px solid #30363d; text-align: left; overflow-wrap: break-word; line-height: 1.2; max-height: 150px; overflow-y: auto; }
    </style>
</head>
<body>
    <h2>CENTRAL GHOST v7.0</h2>
    
    <div class="flex-container">
        <div class="box-mini">
            <h3>MOD 01: BUSCA</h3>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-orange">SOCIAL</a>
        </div>
        <div class="box-mini">
            <h3>MOD 02: TÉCNICO</h3>
            <a href="https://www.ipqualityscore.com/" target="_blank" class="btn btn-red">IP SCAN</a>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ</a>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE</a>
        </div>

        <div class="box-full">
            <h3>MOD 04: SENTINELA DE LINKS (URL SCAN)</h3>
            <form action="/scan_url" method="post">
                <input type="text" name="url" placeholder="Cole o link suspeito aqui..." required>
                <button type="submit" class="btn btn-purple">VERIFICAR REPUTAÇÃO</button>
            </form>
            {% if u %}
            <div class="status-badge {{ 'fraude' if u.risco == 'ALTO' else 'real' }}">
                [{{ u.risco }}] {{ u.titulo }}
                <p style="font-size: 0.6rem; font-weight: normal; margin-top:5px;">Domínio: {{ u.dominio }}</p>
                <div class="dados-container"><strong>REPORTE SENTINELA:</strong><br>{{ u.msg }}</div>
            </div>
            {% endif %}
        </div>

        <div class="box-full">
            <h3>MOD 03: SCANNER OCR ELITE (PDF/FOTO)</h3>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf, .jpg, .jpeg, .png" style="font-size:0.7rem; margin: 10px 0; color:#8b949e;" required>
                <button type="submit" class="btn btn-green">EXECUTAR PERÍCIA</button>
            </form>
            {% if r %}
            <div class="status-badge {{ 'fraude' if r.status == 'A' else 'real' }}">
                {{ r.titulo }}
                <div class="dados-container">{{ r.dados }}</div>
            </div>
            {% endif %}
        </div>
    </div>
    <p style="margin-top: 15px; font-size: 0.5rem; color: #484f58;">SISTEMA PRIVATIVO | GHOST INTEL</p>
</body>
</html>
"""

def motor_analise(caminho):
    texto = ""
    try:
        ext = caminho.lower().split('.')[-1]
        if ext == 'pdf':
            with open(caminho, "rb") as f:
                pdf = pypdf.PdfReader(f); [ (texto := texto + pg.extract_text().upper() + " ") for pg in pdf.pages ]
        if not texto.strip() or ext in ['jpg', 'jpeg', 'png']:
            texto = " ".join(reader.readtext(caminho, detail=0)).upper()
    except: return {"status": "A", "titulo": "⚠️ FALHA", "dados": "Erro no OCR"}

    res = " ".join(texto.split())[:800]
    if "AGENDAMENTO" in texto:
        return {"status": "A", "titulo": "🚨 GOLPE: PIX AGENDADO", "dados": res}
    return {"status": "O", "titulo": "🔍 ANÁLISE CONCLUÍDA", "dados": res}

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.form.get('url')
    domain = urlparse(url).netloc if "://" in url else urlparse("http://"+url).netloc
    
    # Simulação de base de dados de Phishing e Shady TLDs
    shady_tlds = ['.xyz', '.top', '.zip', '.icu', '.link', '.bet', '.win']
    blacklist = ['brazino777', 'login', 'atualizar-dados', 'verificar-pix', 'suporte-bank']
    
    risco = "BAIXO"
    msg = "Domínio parece limpo. Sem detecções imediatas em listas de phishing."
    
    if any(x in domain.lower() for x in shady_tlds):
        risco = "ALTO"
        msg = "EXTENSÃO SUSPEITA (.xyz, .zip, etc). Comum em ataques de malware."
    if any(x in url.lower() for x in blacklist):
        risco = "ALTO"
        msg = "URL contém palavras-chave usadas em PHISHING/GOLPES bancários."
    
    res = {"dominio": domain, "risco": risco, "titulo": "SCANNER DE LINK", "msg": msg}
    return render_template_string(HTML_PAGE, u=res)

@app.route('/analisar', methods=['POST'])
def upload_analise():
    f = request.files.get('file')
    if f:
        p = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(p)
        return render_template_string(HTML_PAGE, r=motor_analise(p))
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
