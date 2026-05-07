import os
from flask import Flask, render_template_string, request, send_from_directory, redirect
import pypdf

app = Flask(__name__)

# Pasta temporária para análise
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
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 8px; text-align: center; }
        
        .header { margin-bottom: 12px; }
        
        /* Container principal */
        .flex-container {
            display: flex;
            flex-direction: row;
            flex-wrap: wrap;
            justify-content: space-between;
            width: 100%;
            margin: 0 auto;
        }

        /* Força Blocos 01 e 02 lado a lado (48% cada) */
        .box-mini { 
            border: 1px solid #30363d; 
            border-radius: 8px; 
            padding: 10px; 
            background: #161b22; 
            text-align: left; 
            width: 48%; 
            margin-bottom: 10px;
        }

        /* Bloco 03 ocupa a largura total embaixo */
        .box-full {
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 12px;
            background: #161b22;
            text-align: left;
            width: 100%;
        }

        .btn {
            display: block; width: 100%; padding: 12px 2px; 
            text-decoration: none; border-radius: 6px; 
            font-weight: bold; margin-top: 8px; 
            text-align: center; color: white; font-size: 0.65rem; 
            text-transform: uppercase; border: none;
        }
        
        .btn-green { background-color: #238636; }
        .btn-purple { background-color: #8957e5; }
        .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; }
        .btn-red { background-color: #da3633; }
        .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        
        h2 { color: #3fb950; font-size: 1rem; margin-bottom: 5px; }
        h3 { color: #8b949e; font-size: 0.55rem; border-bottom: 1px solid #30363d; padding-bottom: 3px; text-transform: uppercase; }
        .label { font-size: 0.5rem; color: #8b949e; margin-top: 8px; font-weight: bold; display: block; }
        
        /* Badges de Status da Análise */
        .status-badge { margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; text-align: center; }
        .fraude { background: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .real { background: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
    </style>
</head>
<body>
    <div class="header">
        <h2>CENTRAL GHOST v4.5</h2>
    </div>
    
    <div class="flex-container">
        <div class="box-mini">
            <h3>MOD 01: BUSCA</h3>
            <span class="label">INVESTIGAÇÃO:</span>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-orange">SOCIAL</a>
        </div>

        <div class="box-mini">
            <h3>MOD 02: TÉCNICO</h3>
            <span class="label">SCANNER:</span>
            <a href="https://www.ipqualityscore.com/" target="_blank" class="btn btn-red">IP SCAN</a>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ</a>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE</a>
        </div>

        <div class="box-full">
            <h3>MOD 03: ANALISADOR DE PIX</h3>
            <span class="label">UPLOAD DE COMPROVANTE (PDF):</span>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" style="font-size:0.6rem; margin: 10px 0; color:#8b949e;" required>
                <button type="submit" class="btn btn-green" style="font-size: 0.8rem; padding: 15px;">ESCANEAR & ANALISAR</button>
            </form>
            
            {% if resultado %}
            <div class="status-badge {{ 'fraude' if resultado.fraude else 'real' }}">
                {{ "⚠️ ALERTA: POSSÍVEL GOLPE" if resultado.fraude else "✅ COMPROVANTE REAL" }}
                <p style="font-size: 0.6rem; font-weight: normal; margin-top:5px;">{{ resultado.mensagem }}</p>
            </div>
            {% endif %}
        </div>
    </div>
    <p style="margin-top: 15px; font-size: 0.5rem; color: #484f58;">OPERACIONAL | GHOST INTEL</p>
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
        return {"fraude": True, "mensagem": "Erro técnico ao ler o PDF."}

    is_fraude = False
    motivo = "Padrões de segurança bancária identificados corretamente."

    # Regras Forenses GHOST
    if "AGENDAMENTO" in texto and "COMPROVANTE" in texto:
        is_fraude = True
        motivo = "O arquivo tenta passar um AGENDAMENTO como se fosse um pagamento concluído."
    elif "ID" not in texto and "AUTENTICACAO" not in texto and "TRANSACAO" not in texto:
        is_fraude = True
        motivo = "Faltam códigos de ID ou Autenticação Digital necessários."
    
    return {"fraude": is_fraude, "mensagem": motivo}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/analisar', methods=['POST'])
def upload_analise():
    file = request.files.get('file')
    if file and file.filename != '':
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        resultado = motor_analise(path)
        return render_template_string(HTML_PAGE, resultado=resultado)
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
