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
            padding: 20px; 
            text-align: center;
        }
        .container { max-width: 450px; margin: 0 auto; }
        .header { margin-bottom: 25px; padding-top: 10px; }
        .box { 
            border: 2px solid #30363d; 
            border-radius: 12px; 
            padding: 15px; 
            background: #161b22; 
            text-align: left; 
            margin-bottom: 20px;
        }
        .btn {
            display: block; 
            width: 100%; 
            padding: 15px; 
            text-decoration: none; 
            border-radius: 8px; 
            font-weight: bold; 
            margin-top: 12px; 
            text-align: center; 
            color: white; 
            font-size: 1rem;
            transition: 0.3s;
        }
        .btn:active { transform: scale(0.98); }
        
        .btn-green { background-color: #238636; }
        .btn-purple { background-color: #8957e5; }
        .btn-orange { background-color: #d29922; }
        .btn-blue { background-color: #0969da; }
        .btn-red { background-color: #da3633; }
        .btn-dark { background-color: #30363d; border: 1px solid #8b949e; }
        
        h2 { color: #3fb950; margin-bottom: 5px; }
        h3 { color: #8b949e; font-size: 0.9rem; margin-bottom: 10px; border-bottom: 1px solid #30363d; padding-bottom: 5px; }
        .label { font-size: 0.75rem; color: #8b949e; margin-top: 10px; font-weight: bold; display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Painel OSINT GHOST</h2>
            <p style="font-size: 0.8rem; color: #8b949e;">V2.5 - Módulo Anti-Fraude</p>
        </div>
        
        <div class="box">
            <h3>MÓDULO 01: BUSCA ATIVA</h3>
            <span class="label">IDENTIDADE & EMAIL:</span>
            <a href="https://epieos.com" target="_blank" class="btn btn-green">EPIEOS</a>
            <a href="https://intelx.io" target="_blank" class="btn btn-purple">INTELX</a>

            <span class="label">REDES SOCIAIS:</span>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-orange">SOCIAL SEARCHER</a>
        </div>

        <div class="box">
            <h3>MÓDULO 02: ANÁLISE TÉCNICA</h3>
            <span class="label">FRAUDE & LOCALIZAÇÃO:</span>
            <a href="https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test" target="_blank" class="btn btn-red">IP QUALITY SCORE</a>
            
            <span class="label">DADOS EMPRESARIAIS:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-blue">CNPJ.BIZ</a>
        </div>

        <div class="box" style="border-style: dashed; opacity: 0.8;">
            <a href="https://www.google.com" target="_blank" class="btn btn-dark">GOOGLE SEARCH (AUXILIAR)</a>
        </div>

        <p style="margin-top: 20px; font-size: 0.6rem; color: #484f58;">STATUS: SISTEMA CRIPTOGRAFADO</p>
    </div>
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
