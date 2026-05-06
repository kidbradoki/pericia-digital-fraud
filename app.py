import os
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML Ajustado para Perícia Digital
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
            padding: 20px; 
            text-align: center;
            overflow-x: hidden;
        }
        .dossie-box { 
            border: 2px solid #2ea043; 
            border-radius: 10px; 
            padding: 20px; 
            margin-top: 20px; 
            background: #161b22;
            word-wrap: break-word;
        }
        .btn-link {
            display: inline-block;
            background-color: #238636;
            color: white;
            padding: 15px 25px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 20px;
            border: none;
        }
    </style>
</head>
<body>
    <h1>Painel de Perícia</h1>
    <div class="dossie-box">
        <p style="color: #3fb950; font-weight: bold;">[ RELATÓRIO OSINT GERADO ]</p>
        <br>
        <p>Alvo identificado nas bases públicas.</p>
        <p>Clique abaixo para acessar o Neoral:</p>
        
        <a href="https://osint.neoral.com" target="_blank" class="btn-link">
            ABRIR NO NEORAL
        </a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # O Render exige ler a porta da variável de ambiente
    # Se não encontrar, ele usa a 10000 como padrão
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
