import os
from flask import Flask, render_template_string, request, send_from_directory, redirect, url_for
import pypdf

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
        
        .flex-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }

        .box { 
            border: 1px solid #30363d; 
            border-radius: 10px; 
            padding: 12px; 
            background: #161b22; 
            text-align: left; 
            flex: 1 1 45%; /* Mantém os dois de cima lado a lado */
            min-width: 300px;
        }

        .box-full {
            flex: 1 1 100%; /* Faz o bloco do Pix ocupar a largura total embaixo */
        }

        .btn {
            display: block; 
            width: 100%; 
            padding: 14px; 
            text-decoration: none; 
            border-radius: 8px; 
            font-weight: bold; 
            margin-top: 10px; 
            text-align: center; 
            color: white; 
            font-size: 0.8rem; 
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
        
        h2 { color: #3fb950; font-size: 1.2rem; }
        h3 { 
            color: #8b949e; 
            font-size: 0.7rem; 
            margin-bottom: 8px; 
            border-bottom: 1px solid #30363d; 
            padding-bottom: 5px; 
            text-transform: uppercase;
        }
        .label { font-size: 0.6rem; color: #8b949e; margin-top: 10px; font-weight: bold; display: block; }
        
        .status-badge {
            margin-top: 10px;
            padding: 10px;
            border-radius: 6px;
            font-weight: bold;
            font-size: 0.9rem;
            text-align: center;
        }
        .fraude { background-color: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .real { background-color: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
    </style>
</head>
<body>
    <div class="header">
        <h2>OSINT GHOST - CENTRAL</h2>
        <p style="font-size: 0.7rem; color: #8b949e;">Operação Forense v4.2</p>
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
            <a href="https://www.ipqualityscore.com/" target="_blank" class="btn btn-red">IP QUALITY</a>
            <span class="label">DADOS CORPORATIVOS:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ.BIZ</a>
            <span class="label">AUXILIAR:</span>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE SEARCH</a>
        </div>

        <div class="box box-full">
            <h3>MÓDULO 03: FORENSE PIX</h3>
            <span class="label">UPLOAD DE COMPROVANTE (PDF):</span>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" style="margin: 10px 0; color:#8b949e;" required>
                <button type="submit" class="btn btn-green">ESCANEAR & ANALISAR</button>
            </form>
            
            {% if resultado %}
            <div class="status-badge {{ 'fraude' if resultado.fraude else 'real' }}">
                {{ "⚠️ ALERTA: POSSÍVEL GOLPE/FRAUDE DETECTADO" if resultado.fraude else "✅ PADRÃO DE COMPROVANTE REAL" }}
                <p style="font-size: 0.65rem; font-weight: normal; margin-top:5px;">{{ resultado.mensagem }}</p>
            </div>
            <a href="{{ url_for('download_file', filename=filename) }}" class="btn btn-blue">DOWNLOAD ARQUIVO</a>
            {% endif %}
        </div>
    </div>

    <p style="margin-top: 20px; font-size: 0.55rem; color: #484f58;">STATUS: SISTEMA CRIPTOGRAFADO | GHOST ATIVO</p>
</body>
</html>
"""

def motor_analise(caminho):
    texto = ""
    try:
        with open(caminho, "rb") as f:
            pdf = pypdf.PdfReader(f)
            for pagina in pdf.pages:
                texto += pagina.extract_text().upper()
    except:
        return {"fraude": True, "mensagem": "Erro na leitura forense do arquivo."}

    # Critérios de Análise GHOST
    is_fraude = False
    motivo = "Os dados textuais condizem com um comprovante emitido por instituição bancária."

    if "AGENDAMENTO" in texto and "COMPROVANTE DE PAGAMENTO" in texto:
        is_fraude = True
        motivo = "O documento contém termos de AGENDAMENTO disfarçados de COMPROVANTE."
    elif "ID" not in texto and "AUTENTICACAO" not in texto and "TRANSACAO" not in texto:
        is_fraude = True
        motivo = "Faltam códigos de autenticação digital obrigatórios."
    
    return {"fraude": is_fraude, "mensagem": motivo}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/analisar', methods=['POST'])
def upload_analise():
    file = request.files.get('file')
    if file and file.filename != '':
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        resultado = motor_analise(path)
        return render_template_string(HTML_PAGE, resultado=resultado, filename=filename)
    return redirect('/')

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
