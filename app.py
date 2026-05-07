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
            font-family: sans-serif; 
            padding: 10px; 
            text-align: center;
        }
        .header { margin-bottom: 15px; }
        
        /* Container que força o lado a lado */
        .flex-container {
            display: flex;
            flex-direction: row; /* Força linha única */
            justify-content: center;
            gap: 8px; /* Espaço pequeno entre blocos */
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
        }

        .box { 
            border: 1px solid #30363d; 
            border-radius: 10px; 
            padding: 10px; 
            background: #161b22; 
            text-align: left; 
            flex: 1; /* Faz ambos ocuparem o mesmo espaço (50/50) */
            min-width: 0; /* Impede que o bloco estoure o limite da tela */
        }

        .btn {
            display: block; 
            width: 100%; 
            padding: 12px 2px; 
            text-decoration: none; 
            border-radius: 6px; 
            font-weight: bold; 
            margin-top: 8px; 
            text-align: center; 
            color: white; 
            font-size: 0.75rem; /* Fonte menor para caber lado a lado */
            text-transform: uppercase;
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
            font-size: 0.65rem; 
            margin-bottom: 5px; 
            border-bottom: 1px solid #30363d; 
            padding-bottom: 3px; 
            white-space: nowrap; 
            overflow: hidden;
            text-overflow: ellipsis;
        }
        .label { font-size: 0.6rem; color: #8b949e; margin-top: 8px; font-weight: bold; display: block; }
    </style>
</head>
<body>
    <div class="header">
        <h2>OSINT GHOST</h2>
        <p style="font-size: 0.7rem; color: #8b949e;">Central de Inteligência v2.7</p>
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
            <span class="label">TÉCNICO/IP:</span>
            <a href="https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test" target="_blank" class="btn btn-red">IP QUALITY</a>
            <span class="label">CNPJ:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ.BIZ</a>
            <span class="label">BUSCA:</span>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE</a>
        </div>
    </div>

    <p style="margin-top: 20px; font-size: 0.55rem; color: #484f58;">AGENTE: GHOST | OPERAÇÃO ATIVA</p>
</body>
</html>
"""

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
