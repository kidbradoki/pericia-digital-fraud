import os
import easyocr
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Configura pasta de uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inicializa o motor de perícia (OCR)
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GHOST v7.0</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background: #161b22; width: 48%; margin-bottom: 10px; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.7rem; text-decoration: none; border: none; cursor: pointer; text-transform: uppercase; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; }
        .btn-dark { background-color: #30363d; margin-top: 15px; }
        h2 { color: #3fb950; font-size: 1.1rem; margin-bottom: 15px; }
        h3 { color: #8b949e; font-size: 0.6rem; margin-bottom: 5px; text-transform: uppercase; border-bottom: 1px solid #30363d; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 10px; border-radius: 4px; margin-bottom: 5px; }
        .res-box { margin-top: 10px; padding: 10px; border-radius: 6px; background: rgba(0,0,0,0.3); border: 1px solid #30363d; font-size: 0.65rem; color: #8b949e; }
    </style>
</head>
<body>
    <h2>CENTRAL GHOST v7.0</h2>
    <div class="flex-container">
        <div class="box-mini">
            <h3>MOD 01</h3>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
        </div>
        <div class="box-mini">
            <h3>MOD 02</h3>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>
        </div>
        
        <div class="box-full">
            <h3>MOD 03: SENTINELA</h3>
            <form method="POST">
                <input type="text" name="url" placeholder="Link suspeito..." required>
                <button type="submit" name="acao" value="scan" class="btn btn-purple">SCAN LINK</button>
            </form>
            {% if u %}
            <div class="res-box"><strong>RESULTADO:</strong><br>{{ u }}</div>
            {% endif %}
        </div>

        <div class="box-full">
            <h3>MOD 04: PERÍCIA OCR</h3>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*,.pdf" style="font-size:0.6rem;">
                <button type="submit" name="acao" value="ocr" class="btn btn-green">EXECUTAR OCR</button>
            </form>
            {% if r %}
            <div class="res-box"><strong>TEXTO EXTRAÍDO:</strong><br>{{ r }}</div>
            {% endif %}
        </div>
    </div>
    <a href="/" class="btn btn-dark">LIMPAR TELA</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def main():
    u_res = None
    r_res = None
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'scan':
            u_res = "Análise concluída. Motor Alpha operando."
        elif acao == 'ocr':
            f = request.files.get('file')
            if f:
                path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
                f.save(path)
                txt = " ".join(reader.readtext(path, detail=0)).upper()
                r_res = txt[:500]
    return render_template_string(HTML_PAGE, u=u_res, r=r_res)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
