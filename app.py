import os
from flask import Flask, render_template_string

app = Flask(__name__)

# CSS e HTML integrados para evitar erro de carregamento
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 20px; overflow-x: hidden; }
        .card { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .dossie { border: 2px solid #2ea043; border-radius: 8px; padding: 15px; background: #0d1117; word-wrap: break-word; }
        .link-osint { color: #58a6ff; font-weight: bold; text-decoration: underline; word-break: break-all; font-size: 1.1rem; }
        h2 { margin-bottom: 15px; text-align: center; }
    </style>
</head>
<body>
    <h2>Central de Perícia Digital</h2>
    <div class="card">
        <h3>Rastreio OSINT</h3>
        <br>
        <div class="dossie">
            <p style="color:#3fb950;"><b>[ RESULTADO DA ANÁLISE ]</b></p><br>
            <p>✅ ALVO IDENTIFICADO</p>
            <p>🔎 VARREDURA: Bases Públicas</p><br>
            <p>🌐 <b>CLIQUE NO LINK ABAIXO PARA O RELATÓRIO:</b></p>
            <a href="https://osint.neoral.com" target="_blank" class="link-osint">https://osint.neoral.com</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # O Render exige que a porta seja lida da variável de ambiente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
