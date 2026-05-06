import os
from flask import Flask, render_template_string

app = Flask(__name__)

# HTML blindado: Resolve a proporção da tela e o link do Neoral
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Painel de Perícia</title>
    <style>
        /* Bloqueio de vazamento lateral */
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body { 
            background-color: #0d1117; 
            color: #c9d1d9; 
            font-family: 'Segoe UI', sans-serif; 
            padding: 20px; 
            overflow-x: hidden; 
        }

        .card { 
            background: #161b22; 
            border: 1px solid #30363d; 
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 15px; 
            width: 100%;
        }

        /* Caixa do Dossiê (Verde) com quebra de linha forçada */
        .dossie-box { 
            border: 2px solid #2ea043; 
            border-radius: 8px; 
            padding: 15px; 
            background: #0d1117; 
            word-wrap: break-word; 
            overflow-wrap: break-word; 
            font-family: monospace;
        }

        .titulo-verde { 
            color: #3fb950; 
            font-weight: bold; 
            text-align: center; 
            margin-bottom: 15px; 
            border-bottom: 1px solid #2ea043;
            padding-bottom: 10px;
        }

        /* Botão para o Neoral - Mais seguro que link comum no Kodular */
        .btn-link {
            display: block;
            width: 100%;
            background-color: #238636;
            color: white;
            text-align: center;
            padding: 15px;
            margin-top: 15px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <div class="card">
        <h2>Rastreio OSINT</h2>
        <br>
        <div class="dossie-box">
            <div class="titulo-verde">DOSSIÊ DE FONTES ABERTAS</div>
            <p>✅ <b>STATUS:</b> Alvo Identificado</p>
            <p>🔎 <b>VARREDURA:</b> Bases Públicas</p>
            <br>
            <p>🌐 <b>ACESSO AO RELATÓRIO:</b></p>
            
            <a href="https://osint.neoral.com" target="_blank" class="btn-link">
                ABRIR NO NEORAL
            </a>
        </div>
    </div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # Configuração vital para o Render ler a porta corretamente
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
