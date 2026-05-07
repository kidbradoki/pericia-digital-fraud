import os
from flask import Flask, render_template_string, request, send_from_directory, redirect
import pypdf

app = Flask(__name__)

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
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 10px; text-align: center; }
        .header { margin-bottom: 15px; }
        .flex-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; width: 100%; max-width: 1000px; margin: 0 auto; }
        .box { border: 1px solid #30363d; border-radius: 10px; padding: 10px; background: #161b22; text-align: left; flex: 1 1 300px; min-width: 280px; margin-bottom: 10px; }
        .btn { display: block; width: 100%; padding: 12px 2px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 8px; text-align: center; color: white; font-size: 0.75rem; text-transform: uppercase; border: none; cursor: pointer; }
        .btn-green { background-color: #238636; }
        .btn-blue { background-color: #0969da; }
        .btn-red { background-color: #da3633; }
        .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        h2 { color: #3fb950; font-size: 1.1rem; }
        h3 { color: #8b949e; font-size: 0.65rem; border-bottom: 1px solid #30363d; padding-bottom: 3px; text-transform: uppercase; }
        .label { font-size: 0.55rem; color: #8b949e; margin-top: 8px; font-weight: bold; display: block; }
        .analise-box { margin-top: 10px; padding: 10px; border-radius: 6px; font-size: 0.75rem; line-height: 1.4; }
        .alerta-fraude { background-color: rgba(218, 54, 51, 0.2); border: 1px solid #da3633; color: #ff7b72; }
        .sucesso-real { background-color: rgba(35, 134, 54, 0.2); border: 1px solid #238636; color: #7ee787; }
    </style>
</head>
<body>
    <div class="header">
        <h2>OSINT GHOST - CENTRAL</h2>
        <p style="font-size: 0.7rem; color: #8b949e;">Análise Forense Avançada v4.0</p>
    </div>
    
    <div class="flex-container">
        <div class="box">
            <h3>RECONHECIMENTO & TÉCNICO</h3>
            <a href="https://epieos.com" target="_blank" class="btn btn-blue">EPIEOS</a>
            <a href="https://www.ipqualityscore.com/" target="_blank" class="btn btn-red">IP QUALITY</a>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-dark">CNPJ.BIZ</a>
        </div>

        <div class="box">
            <h3>MÓDULO 03: DETECTOR DE FRAUDE PIX</h3>
            <span class="label">SUBIR COMPROVANTE PARA ANÁLISE:</span>
            <form action="/analisar" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf" style="font-size:0.6rem; margin-top:5px;" required>
                <button type="submit" class="btn btn-green">ESCANEAR VERACIDADE</button>
            </form>
            
            {% if resultado %}
            <div class="analise-box {{ 'alerta-fraude' if resultado.fraude else 'sucesso-real' }}">
                <strong>STATUS: {{ "⚠️ SUSPEITA DE GOLPE" if resultado.fraude else "✅ PADRÃO IDENTIFICADO" }}</strong><br>
                <p style="margin-top:5px;">{{ resultado.mensagem }}</p>
                <hr style="margin:5px 0; border:0; border-top:1px solid rgba(255,255,255,0.1);">
                <strong>DADOS EXTRAÍDOS:</strong><br>
                {{ resultado.dados }}
            </div>
            <a href="{{ url_for('download_file', filename=filename) }}" class="btn btn-dark" style="margin-top:10px;">BAIXAR CÓPIA ANALISADA</a>
            {% endif %}
        </div>
    </div>
    <p style="margin-top: 15px; font-size: 0.55rem; color: #484f58;">GHOST INTEL | ANÁLISE DE CAMADA 7 ATIVA</p>
</body>
</html>
"""

def analisar_pix(caminho_pdf):
    texto = ""
    try:
        with open(caminho_pdf, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                texto += page.extract_text()
    except:
        return {"fraude": True, "mensagem": "Erro ao ler PDF. Arquivo pode estar corrompido ou protegido.", "dados": "N/A"}

    # Lógica de Detecção de Fraude (Simplificada para o Agente)
    texto_upper = texto.upper()
    fraude = False
    motivos = []

    # Exemplos de gatilhos de fraude comuns em comprovantes falsos
    if "AGENDAMENTO" in texto_upper and "COMPROVANTE DE PAGAMENTO" in texto_upper:
        fraude = True
        motivos.append("O arquivo mistura termos de agendamento com pagamento efetuado.")
    
    if "VALOR" not in texto_upper or "ID DA TRANSACAO" not in texto_upper:
        if "ID" not in texto_upper and "AUTENTICACAO" not in texto_upper:
            fraude = True
            motivos.append("Faltam elementos obrigatórios (ID/Autenticação Bancária).")

    # Extração de dados básica para o Ghost ver
    dados_resumo = f"Conteúdo detectado: {texto[:100]}..."
    
    msg = " | ".join(motivos) if motivos else "Os padrões textuais básicos coincidem com um comprovante real."
    
    return {"fraude": fraude, "mensagem": msg, "dados": dados_resumo}

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/analisar', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return redirect("/")
    file = request.files['file']
    if file.filename == '': return redirect("/")
    if file:
        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        relatorio = analisar_pix(path)
        return render_template_string(HTML_PAGE, resultado=relatorio, filename=filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
