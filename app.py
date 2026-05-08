import os
import easyocr
from flask import Flask, render_template_string, request
from urllib.parse import urlparse

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Motor de Perícia (Carrega uma vez)
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 8px; background: #161b22; width: 48%; margin-bottom: 10px; text-align: left; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px; border-radius: 6px; font-weight: bold; margin-top: 5px; text-align: center; color: white; font-size: 0.65rem; text-decoration: none; border: none; cursor: pointer; text-transform: uppercase; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; } .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; } .btn-red { background-color: #da3633; } .btn-dark { background-color: #30363d; }
        h2 { color: #3fb950; font-size: 1rem; margin-bottom: 10px; }
        h3 { color: #8b949e; font-size: 0.55rem; border-bottom: 1px solid #30363d; margin-bottom: 5px; padding-bottom: 2px; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 8px; border-radius: 4px; font-size: 0.7rem; }
        .result { background: #000; padding: 8px; border-radius: 4px; margin-top: 8px; font-family: monospace; font-size: 0.6rem; border-left: 2px solid #3fb950; overflow-y: auto; max-height: 100px; }
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
            <form method="POST">
                <input type="text" name="url" placeholder="Link suspeito..." required>
                <button type="submit" name="acao" value="scan" class="btn btn-purple">VERIFICAR</button>
            </form>
            {% if u %}<div class="result">{{ u }}</div>{% endif %}
        </div>

        <div class="box-full">
            <h3>MOD 04: SCANNER OCR</h3>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*,.pdf" style="font-size:0.6rem; color:#8b949e;">
                <button type="submit" name="acao" value="ocr" class="btn btn-green">EXECUTAR PERÍCIA</button>
            </form>
            {% if r %}<div class="result">{{ r }}</div>{% endif %}
        </div>
    </div>

    <a href="/" style="color: #8b949e; text-decoration: none; font-size: 0.6rem; display: block; margin-top: 10px;">[ REINICIAR SISTEMA ]</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    u, r = None, None
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'scan':
            url = request.form.get('url', '')
            domain = urlparse(url).netloc if "://" in url else urlparse("http://"+url).netloc
            u = f"DOMÍNIO: {domain} | Análise concluída."
        elif acao == 'ocr':
            f = request.files.get('file')
            if f:
                p = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(p)
                txt = " ".join(reader.readtext(p, detail=0)).upper()
                r = txt[:500]
    return render_template_string(HTML_PAGE, u=u, r=r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
