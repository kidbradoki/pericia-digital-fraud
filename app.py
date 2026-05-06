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
            padding: 15px; 
            text-align: center;
        }
        .header { margin-bottom: 20px; padding-top: 10px; }
        
        /* Layout em Grade Flexível */
        .flex-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 15px;
            max-width: 1000px;
            margin: 0 auto;
        }

        .box { 
            border: 2px solid #30363d; 
            border-radius: 12px; 
            padding: 15px; 
            background: #161b22; 
            text-align: left; 
            flex: 1 1 300px; /* Base de 300px, cresce se houver espaço */
            max-width: 450px;
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
            font-size: 0.95rem;
            transition: 0.2s;
        }
        .btn:active { transform: scale(0.97); }
        
        .btn-green { background-color: #238636; }
        .btn-purple { background-color: #8957e5; }
        .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; }
        .btn-red { background-color: #da3633; }
        .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        
        h2 { color: #3fb950; margin-bottom: 5px; }
        h3 { color: #8b949e; font-size: 0.85rem; margin-bottom: 10px; border-bottom: 1px solid #30363d; padding-bottom: 5px; text-transform: uppercase; }
        .label { font-size: 0.7rem; color: #8b949e; margin-top: 10px; font-weight: bold; display: block; }
    </style>
</head>
<body>
    <div class="header">
        <h2>Painel OSINT GHOST</h2>
        <p style="font-size: 0.8rem; color: #8b949e;">Central de Inteligência v2.6</p>
    </div>
    
    <div class="flex-container">
        <div class="box">
            <h3>Módulo 01: Reconhecimento</h3>
            <span class="label">IDENTIDADE & EMAIL:</span>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>

            <span class="label">REDES SOCIAIS:</span>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-orange">SOCIAL SEARCHER</a>
        </div>

        <div class="box">
            <h3>Módulo 02: Perícia Técnica</h3>
            <span class="label">ANÁLISE DE RISCO (IP):</span>
            <a href="https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test" target="_blank" class="btn btn-red">IP QUALITY SCORE</a>
            
            <span class="label">DADOS CORPORATIVOS:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ.BIZ</a>

            <span class="label">OUTROS:</span>
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE SEARCH</a>
        </div>
    </div>

    <p style="margin-top: 25px; font-size: 0.6rem; color: #484f58;">AGENTE: GHOST | SISTEMA ATIVO</p>
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
