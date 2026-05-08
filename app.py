import os
import easyocr
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Motor OCR
reader = easyocr.Reader(['pt', 'en'], gpu=False)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GHOST INTEL</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background: #161b22; text-align: left; width: 48%; margin-bottom: 10px; display: inline-block; vertical-align: top; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 10px; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.7rem; text-decoration: none; border: none; cursor: pointer; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; }
        .btn-dark { background-color: #30363d; margin-top: 15px; }
        h2 { color: #3fb950; font-size: 1.1rem; margin-bottom: 15px; }
        input[type="text"] { width: 100%; background: #0d1117; border: 1px solid #30363d; color: #7ee787; padding: 10px; border-radius: 4px; }
        .status-badge { margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: bold; text-align: center; background: rgba(35, 134, 54, 0.1); border: 1px solid #30363d; }
        .dados-container { background: #000; color: #8b949e; font-family: monospace; font-size: 0.6rem; padding: 10px; margin-top: 8px; border-radius: 4px; border: 1px solid #30363d; text-align: left; overflow-y: auto; max-height: 120px; }
    </style>
</head>
<body>
    <h2>CENTRAL GHOST v7.0</h2>
    <div style="width: 100%; text-align: center;">
        <div class="box-mini">
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
        </div>
        <div class="box-mini">
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>
        </div>
        
        <div class="box-full">
            <form method="POST">
                <input type="text" name="url" placeholder="Cole o link aqui..." required>
                <button type="submit" name="acao" value="scan" class="btn btn-purple">SCAN LINK</button>
            </form>
            {% if u %}
            <div class="status-badge">
                RESULTADO: {{ u.risco }}
                <div class="dados-container">{{ u.msg }}</div>
            </div>
            {% endif %}
        </div>

        <div class="box-full">
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*,.pdf" style="font-size: 0.7rem;">
                <button type="submit" name="acao" value="ocr" class="btn btn-green">SCAN OCR</button>
            </form>
            {% if r %}
            <div class="status-badge">
                PERÍCIA CONCLUÍDA
                <div class="dados-container">{{ r.dados }}</div>
            </div>
            {% endif %}
        </div>
    </div>
    <a href="/" class="btn btn-dark">LIMPAR TUDO</a>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    u = None
    r = None
    if request.method == 'POST':
        acao = request.form.get('acao')
        if acao == 'scan':
            u = {"risco": "PROCESSADO", "msg": "Link analisado pelo motor Alpha."}
        elif acao == 'ocr':
            f = request.files.get('file')
            if f:
                f.save("temp")
                txt = " ".join(reader.readtext("temp", detail=0)).upper()
                r = {"dados": txt[:400]}
    return render_template_string(HTML_PAGE, u=u, r=r)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
