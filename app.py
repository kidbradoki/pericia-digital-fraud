import os
import pypdf
import easyocr
from flask import Flask, render_template_string, request, redirect, url_for
from urllib.parse import urlparse

app = Flask(__name__)

# Configuração de Pastas
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Motor OCR
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>CENTRAL GHOST</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; width: 100%; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background: #161b22; text-align: left; width: 48%; margin-bottom: 10px; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px 2px; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.65rem; text-transform: uppercase; text-decoration: none; border: none; cursor: pointer; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; } .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; } .btn-red { background-color: #da3633; } .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        h2 { color: #3fb950; font-size: 1rem; margin-bottom: 10px; text-transform: uppercase; }
        h3 { color: #8b949e; font-size: 0.55rem; border-bottom: 1px solid #30363d; padding-bottom: 3px; text-transform: uppercase; margin-bottom: 5px; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 8px; border-radius: 4px; font-size: 0.7rem; }
        .status-badge { margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; text-align: center; }
        .fraude { background: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .real { background: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
        .dados-container { background: #000; color: #8b949e; font-family: monospace; font-size: 0.55rem; padding: 10px; margin-top: 8px; border-radius: 4px; border: 1px solid #30363d; text-align: left; overflow-y: auto; max-height: 150px; }
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
            <h3>MOD 03: SENTINELA DE LINKS</h3>
            <form action="/scan_url" method="post">
                <input type="text" name="url" placeholder="Cole o link suspeito aqui..." required>
                <button type="submit" class="btn btn-purple">VERIFICAR REPUTAÇÃO</button>
            </form>
            {% if u %}
            <div class="status-badge {{ 'fraude' if u.risco == 'ALTO' else 'real' }}">
                [{{ u.risco }}] {{ u.titulo }}
                <div class="dados-container">{{ u.msg }}</div>
                <a href="/" class="btn btn-dark" style="margin-top:5px;">LIMPAR RESULTADO</a>
            </div>
            {% endif %}
        </div>

        <div class="box-full">
            <h3>MOD 04: SCANNER OCR ELITE</h3>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf, .jpg, .jpeg, .png" required>
                <button type="submit" class="btn btn-green">EXECUTAR PERÍCIA</button>
            </form>
            {% if r %}
            <div class="status-badge {{ 'fraude' if r.status == 'A' else 'real' }}">
                {{ r.titulo }}
                <div class="dados-container">{{ r.dados }}</div>
                <a href="/" class="btn btn-dark" style="margin-top:5px;">LIMPAR RESULTADO</a>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/scan_url', methods=['POST'])
def scan_url():
    url = request.form.get('url', '')
    domain = urlparse(url).netloc if "://" in url else urlparse("http://"+url).netloc
    risco = "ALTO" if any(x in url.lower() for x in ['.xyz', 'brazino', 'pix']) else "BAIXO"
    res = {"dominio": domain, "risco": risco, "titulo": "RESULTADO SCAN", "msg": "Análise concluída com sucesso."}
    return render_template_string(HTML_PAGE, u=res)

@app.route('/analisar', methods=['POST'])
def upload_analise():
    f = request.files.get('file')
    if f:
        p = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(p)
        try:
            texto = " ".join(reader.readtext(p, detail=0)).upper()
            status = "A" if "AGENDAMENTO" in texto else "O"
            res = {"status": status, "titulo": "RESULTADO OCR", "dados": texto[:500]}
        except:
            res = {"status": "A", "titulo": "ERRO", "dados": "Falha no processamento."}
        return render_template_string(HTML_PAGE, r=res)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
