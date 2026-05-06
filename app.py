import os
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML com o botão do Google mantido para diagnóstico e busca
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
            overflow-x: hidden;
        }
        .container {
            max-width: 500px;
            margin: 0 auto;
        }
        .dossie-box { 
            border: 2px solid #2ea043; 
            border-radius: 12px; 
            padding: 20px; 
            margin-top: 20px; 
            background: #161b22;
            word-wrap: break-word;
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
            cursor: pointer;
        }
        .btn-neoral { background-color: #238636; color: white; } /* Verde Perícia */
        .btn-google { background-color: #1f6feb; color: white; }  /* Azul Diagnóstico */
        
        .status-tag {
            background: #238636;
            color: white;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            float: right;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Central de Perícia Digital</h2>
        
        <div class="dossie-box">
            <span class="status-tag">ATIVO</span>
            <p style="color: #3fb950; font-weight: bold; margin-bottom: 15px;">[ RELATÓRIO GERADO ]</p>
            <p>🔎 <b>Varredura:</b> Fontes Abertas</p>
            <p>📡 <b>Servidor:</b> Render Live</p>
            <br>
            
            <a href="https://osint.neoral.com" target="_blank" class="btn btn-neoral">
                ABRIR NO NEORAL
            </a>

            <a href="https://www.google.com" target="_blank" class="btn btn-google">
                TESTAR CONEXÃO / GOOGLE
            </a>
        </div>
        
        <p style="margin-top: 20px; font-size: 0.7rem; color: #8b949e;">
            ID da Sessão: 1000072071-GHOST
        </p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # Garante que a porta seja a correta para o Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
