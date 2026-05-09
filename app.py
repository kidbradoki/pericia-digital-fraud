import os
import easyocr
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Inicializa o OCR (mantenha gpu=False se estiver no Hugging Face Free)
reader = easyocr.Reader(['pt', 'en'], gpu=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    res = None
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                # Lógica de processamento do OCR
                img_bytes = file.read()
                result = reader.readtext(img_bytes, detail=0)
                res = " ".join(result) if result else "Nenhum texto detectado."

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CENTRAL GHOST v7.0</title>
        <style>
            body { 
                background: #0d1117; 
                color: #c9d1d9; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                text-align: center; 
                padding: 20px;
                margin: 0;
            }
            .header { margin-bottom: 30px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
            .header h1 { color: #58a6ff; font-size: 1.5rem; margin: 0; }
            
            .module-box {
                background: #161b22;
                border: 1px solid #30363d;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 15px;
                text-align: left;
            }
            .module-title { color: #8b949e; font-size: 0.8rem; font-weight: bold; margin-bottom: 10px; text-transform: uppercase; }
            
            .btn { 
                background: #238636; 
                color: white; 
                padding: 12px; 
                border-radius: 6px; 
                display: block; 
                width: 100%; 
                margin: 8px 0; 
                text-decoration: none; 
                border: none; 
                font-weight: bold;
                box-sizing: border-box;
                cursor: pointer;
                font-size: 0.9rem;
            }
            .btn-blue { background: #1f6feb; }
            .btn-purple { background: #8957e5; }
            
            input[type="file"] {
                background: #21262d;
                border: 1px solid #30363d;
                color: #8b949e;
                width: 100%;
                padding: 10px;
                border-radius: 6px;
                margin-bottom: 10px;
                box-sizing: border-box;
            }
            .result-box {
                background: #000;
                color: #39ff14;
                padding: 15px;
                border-radius: 6px;
                font-family: monospace;
                margin-top: 15px;
                border: 1px solid #39ff14;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>CENTRAL GHOST v7.0</h1>
        </div>

        <div class="module-box">
            <div class="module-title">Módulo 01: Inteligência de Busca</div>
            <a href="https://epieos.com" target="_blank" class="btn">EPIEOS (E-mail/Phone)</a>
            <a href="https://intelx.io" target="_blank" class="btn">INTELX (Data Leaks)</a>
        </div>

        <div class="module-box">
            <div class="module-title">Módulo 02: Suporte Técnico</div>
            <a href="https://github.com" target="_blank" class="btn btn-blue">REPOSITÓRIOS GITHUB</a>
        </div>

        <div class="module-box">
            <div class="module-title">Módulo 03: Sentinela de Links</div>
            <a href="https://www.virustotal.com" target="_blank" class="btn btn-purple">VERIFICAR URL (VIRUSTOTAL)</a>
        </div>

        <div class="module-box">
            <div class="module-title">Módulo 04: Perícia de Documentos (OCR)</div>
            <form method="POST" enctype="multipart/form-data">
                <input type="file" name="file" accept="image/*">
                <button type="submit" class="btn">ESCANEAR IMAGEM</button>
            </form>
            {% if res %}
            <div class="result-box">
                <strong>RESULTADO DA PERÍCIA:</strong><br>
                {{ res }}
            </div>
            {% endif %}
        </div>

    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7860)
