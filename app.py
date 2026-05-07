import os, re, pypdf
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER): os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# HTML Mantido - Ajustado para aceitar apenas PDF
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .flex-container { display: flex; flex-direction: row; flex-wrap: wrap; justify-content: space-between; width: 100%; }
        .box-mini { border: 1px solid #30363d; border-radius: 8px; padding: 10px; background: #161b22; text-align: left; width: 48%; margin-bottom: 10px; }
        .box-full { border: 1px solid #30363d; border-radius: 8px; padding: 12px; background: #161b22; text-align: left; width: 100%; }
        .btn { display: block; width: 100%; padding: 12px 2px; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.65rem; text-transform: uppercase; text-decoration: none; border: none; }
        .btn-green { background-color: #238636; } .btn-purple { background-color: #8957e5; } .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; } .btn-red { background-color: #da3633; } .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        h2 { color: #3fb950; font-size: 1rem; margin-bottom: 10px; }
        h3 { color: #8b949e; font-size: 0.55rem; border-bottom: 1px solid #30363d; padding-bottom: 3px; text-transform: uppercase; }
        .status-badge { margin-top: 10px; padding: 10px; border-radius: 6px; font-weight: bold; font-size: 0.75rem; text-align: center; }
        .fraude { background: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .real { background: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
        .dados-container { background: #000; color: #8b949e; font-family: monospace; font-size: 0.55rem; padding: 10px; margin-top: 8px; border-radius: 4px; border: 1px solid #30363d; text-align: left; overflow-wrap: break-word; line-height: 1.2; }
    </style>
</head>
<body>
    <h2>CENTRAL GHOST v5.7 LITE</h2>
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
            <h3>MOD 03: FORENSE DIGITAL (PDF)</h3>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" style="font-size:0.6rem; margin: 10px 0; color:#8b949e;" required>
                <button type="submit" class="btn btn-green" style="font-size: 0.8rem; padding: 15px;">ESCANEAR DOCUMENTO</button>
            </form>
            {% if r %}
            <div class="status-badge {{ 'fraude' if r.status == 'A' else 'real' }}">
                {{ r.titulo }}
                <p style="font-size: 0.6rem; font-weight: normal; margin-top:5px;">{{ r.mensagem }}</p>
                <div class="dados-container"><strong>DADOS EXTRAÍDOS:</strong><br><br>{{ r.dados }}</div>
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
            for pg in pdf.pages:
                ext = pg.extract_text()
                if ext: texto += ext.upper() + " "
    except Exception as e:
        return {"status": "A", "titulo": "⚠️ ERRO DE LEITURA", "mensagem": "Arquivo corrompido ou protegido.", "dados": str(e)}

    if not texto.strip(): 
        return {"status": "A", "titulo": "⚠️ DOC "MUDO"", "mensagem": "O PDF é apenas uma imagem. Requer revisão manual.", "dados": "N/A"}
    
    txt_l = " ".join(texto.split())
    res = txt_l[:500] + "..." if len(txt_l) > 500 else txt_l

    # Classificação
    if any(x in texto for x in ["PIX", "TRANSACAO", "COMPROVANTE"]):
        status = "A" if "AGENDAMENTO" in texto else "O"
        tit = "⚠️ GOLPE: PIX AGENDADO" if status == "A" else "✅ PIX IDENTIFICADO"
        return {"status": status, "titulo": tit, "mensagem": "Análise financeira.", "dados": res}
    
    if any(x in texto for x in ["CEDENTE", "SACADO", "BOLETO"]):
        return {"status": "O", "titulo": "✅ BOLETO IDENTIFICADO", "mensagem": "Cobrança detectada.", "dados": res}

    if any(x in texto for x in ["REGISTRO GERAL", "CNH", "CPF", "IDENTIDADE", "CERTIDAO", "TRIBUNAL"]):
        return {"status": "O", "titulo": "✅ DOCUMENTO PESSOAL", "mensagem": "Dados de identificação.", "dados": res}

    return {"status": "A", "titulo": "⚠️ DOC DESCONHECIDO", "mensagem": "Texto extraído. Avalie o conteúdo.", "dados": res}

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/analisar', methods=['POST'])
def upload_analise():
    f = request.files.get('file')
    if f and f.filename != '':
        p = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(p)
        return render_template_string(HTML_PAGE, r=motor_analise(p))
    return redirect('/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
