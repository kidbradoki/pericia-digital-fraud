import os
from flask import Flask, render_template_string, request, send_from_directory, redirect, url_for

app = Flask(__name__)

# Configuração da pasta de uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            background-color: #0d1117; 
            color: #c9d1d9; 
            font-family: sans-serif; 
            padding: 10px; 
            text-align: center;
        }
        .header { margin-bottom: 15px; }
        
        /* Container para 3 Blocos Lado a Lado */
        .flex-container {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: center;
            gap: 8px;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }

        .box { 
            border: 1px solid #30363d; 
            border-radius: 10px; 
            padding: 10px; 
            background: #161b22; 
            text-align: left; 
            flex: 1 1 250px; /* Base de 250px, divide o espaço */
            min-width: 200px;
            margin-bottom: 10px;
        }

        .btn {
            display: block; 
            width: 100%; 
            padding: 10px 2px; 
            text-decoration: none; 
            border-radius: 6px; 
            font-weight: bold; 
            margin-top: 8px; 
            text-align: center; 
            color: white; 
            font-size: 0.7rem; 
            text-transform: uppercase;
            border: none;
            cursor: pointer;
        }
        
        .btn-green { background-color: #238636; }
        .btn-purple { background-color: #8957e5; }
        .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; }
        .btn-red { background-color: #da3633; }
        .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        
        h2 { color: #3fb950; font-size: 1.1rem; }
        h3 { 
            color: #8b949e; 
            font-size: 0.65rem; 
            margin-bottom: 5px; 
            border-bottom: 1px solid #30363d; 
            padding-bottom: 3px; 
            text-transform: uppercase;
        }
        .label { font-size: 0.55rem; color: #8b949e; margin-top: 8px; font-weight: bold; display: block; }
        
        /* Estilo do Form de Upload */
        input[type="file"] {
            font-size: 0.6rem;
            color: #8b949e;
            margin-top: 5px;
            width: 100%;
        }
        .status-msg {
            font-size: 0.6rem;
            margin-top: 5px;
            color: #3fb950;
        }
    </style>
</head>
<body>
    <div class="header">
        <h2>OSINT GHOST - CENTRAL</h2>
        <p style="font-size: 0.7rem; color: #8b949e;">Operação Forense v3.0</p>
    </div>
    
    <div class="flex-container">
        <div class="box">
            <h3>MÓDULO 01</h3>
            <span class="label">INVESTIGAÇÃO:</span>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>
            <span class="label">SOCIAL:</span>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-orange">SOCIAL S.</a>
        </div>

        <div class="box">
            <h3>MÓDULO 02</h3>
            <span class="label">ANÁLISE DE RISCO:</span>
            <a href="https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test" target="_blank" class="btn btn-red">IP QUALITY</a>
            <span class="label">DADOS CORPORATIVOS:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ.BIZ</a>
            <span class="label">AUXILIAR:</span>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE SEARCH</a>
        </div>

        <div class="box">
            <h3>MÓDULO 03: FORENSE PIX</h3>
            <span class="label">UPLOAD DE COMPROVANTE (PDF):</span>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" required>
                <button type="submit" class="btn btn-green">ESCANEAR & SALVAR</button>
            </form>
            
            {% if filename %}
            <div class="status-msg">✓ PDF Escaneado!</div>
            <span class="label">AÇÕES:</span>
            <a href="{{ url_for('download_file', filename=filename) }}" class="btn btn-blue">DOWNLOAD ARQUIVO</a>
            {% endif %}
        </div>
    </div>

    <p style="margin-top: 15px; font-size: 0.55rem; color: #484f58;">STATUS: SISTEMA CRIPTOGRAFADO | GHOST ATIVO</p>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Retorna a página com o botão de download habilitado
        return render_template_string(HTML_PAGE, filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
