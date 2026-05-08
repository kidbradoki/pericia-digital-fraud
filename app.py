import os
import easyocr
from flask import Flask, render_template_string, request

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Carrega o OCR uma única vez
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 15px; text-align: center; }
        .box { border: 1px solid #30363d; border-radius: 8px; padding: 15px; background: #161b22; margin-bottom: 15px; text-align: left; }
        .btn { display: block; width: 100%; padding: 12px; border-radius: 6px; font-weight: bold; margin-top: 10px; text-align: center; color: white; border: none; cursor: pointer; text-transform: uppercase; text-decoration: none; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 10px; border-radius: 4px; }
        h2 { color: #3fb950; margin-bottom: 20px; }
        .result { background: #000; padding: 10px; border-radius: 5px; margin-top: 10px; font-family: monospace; font-size: 0.8rem; border-left: 3px solid #8957e5; }
    </style>
</head>
<body>
    <h2>GHOST INTEL v7.0</h2>
    
    <div class="box">
        <strong>BUSCA RÁPIDA:</strong>
        <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
    </div>

    <div class="box">
        <strong>SENTINELA DE LINKS:</strong>
        <form method="POST">
            <input type="text" name="url" placeholder="Cole o link suspeito..." required>
            <button type="submit" name="acao" value="scan" class="btn btn-purple">ANALISAR LINK</button>
        </form>
        {% if u %} <div class="result">{{ u }}</div> {% endif %}
    </div>

    <div class="box">
        <strong>PERÍCIA DE COMPROVANTES:</strong>
        <form method="POST" enctype="multipart/form-data">
            <input type="file" name="file" accept="image/*,.pdf">
            <button type="submit" name="acao" value="ocr" class="btn btn-green">ESCANEAR ARQUIVO</button>
        </form>
        {% if r %} <div class="result">{{ r }}</div> {% endif %}
    </div>

    <a href="/" style="color: #8b949e; text-decoration: none; font-size: 0.8rem;">[ LIMPAR TUDO ]</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    u, r = None, None
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'scan':
            u = "Link analisado. Verifique a procedência antes de clicar."
        elif acao == 'ocr':
            f = request.files.get('file')
            if f:
                p = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(p)
                txt = " ".join(reader.readtext(p, detail=0)).upper()
                r = txt[:400]
    return render_template_string(HTML_PAGE, u=u, r=r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
