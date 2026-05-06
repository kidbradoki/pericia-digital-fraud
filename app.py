import os
from flask import Flask, render_template_string

app = Flask(__name__)

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
            font-family: 'Segoe UI', sans-serif; 
            padding: 20px; 
            text-align: center;
        }
        .box { 
            border: 2px solid #2ea043; 
            border-radius: 12px; 
            padding: 20px; 
            margin-top: 20px; 
            background: #161b22;
            text-align: left;
        }
        .btn {
            display: block;
            width: 100%;
            padding: 15px;
            text-decoration: none;
            border-radius: 8px;
            font-weight: bold;
            margin-top: 15px;
            text-align: center;
            border: none;
        }
        .btn-osint { background-color: #238636; color: white; } /* Verde */
        .btn-google { background-color: #1f6feb; color: white; }  /* Azul */
        .alert { color: #f85149; font-size: 0.8rem; margin-top: 10px; text-align: center; }
    </style>
</head>
<body>
    <h2>Painel de Perícia Digital</h2>
    
    <div class="box">
        <p style="color: #3fb950; font-weight: bold;">[ RELATÓRIO DISPONÍVEL ]</p>
        <p>A ferramenta anterior (Neoral) está offline.</p>
        <p>Use a alternativa abaixo (Epieos) para busca de e-mail/identidade:</p>
        
        <a href="https://epieos.com" target="_blank" class="btn btn-osint">
            ABRIR DOSSIÊ (EPIEOS)
        </a>

        <a href="https://www.google.com" target="_blank" class="btn btn-google">
            BUSCA MANUAL / GOOGLE
        </a>
        
        <p class="alert">⚠️ O domínio osint.neoral.com não responde.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
