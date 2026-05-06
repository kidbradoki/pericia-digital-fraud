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
        .container { max-width: 500px; margin: 0 auto; }
        
        .box { 
            border: 2px solid #2ea043; 
            border-radius: 12px; 
            padding: 15px; 
            margin-top: 15px; 
            background: #161b22;
            text-align: left;
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
            border: none;
            color: white;
            font-size: 0.9rem;
        }

        /* Cores Temáticas */
        .btn-epieos { background-color: #238636; } /* Verde - E-mails */
        .btn-intelx { background-color: #8957e5; } /* Roxo - Vazamentos */
        .btn-social { background-color: #d29922; } /* Laranja - Social */
        .btn-ip { background-color: #f85149; }     /* Vermelho - IP/Geo */
        .btn-cnpj { background-color: #0969da; }   /* Azul Escuro - CNPJ */
        .btn-google { background-color: #1f6feb; } /* Azul - Busca */
        
        h2 { margin-bottom: 5px; font-size: 1.4rem; }
        .desc { font-size: 0.8rem; color: #8b949e; margin-bottom: 4px; margin-top: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Painel de Perícia Digital</h2>
        <p style="font-size: 0.8rem; color: #3fb950;">[ GHOST - FULL OSINT PACK ]</p>
        
        <div class="box">
            <p class="desc">🔎 E-mail e Identidade:</p>
            <a href="https://epieos.com" target="_blank" class="btn btn-epieos">EPIEOS</a>

            <p class="desc">🗄️ Dados e Vazamentos:</p>
            <a href="https://intelx.io" target="_blank" class="btn btn-intelx">INTELX</a>

            <p class="desc">📱 Redes Sociais:</p>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-social">SOCIAL-SEARCHER</a>

            <p class="desc">📍 Rastreio de IP e Geo:</p>
            <a href="https://ip-api.com" target="_blank" class="btn btn-ip">IP-API (LOCALIZAÇÃO)</a>

            <p class="desc">🏢 Consulta de Empresas (CNPJ):</p>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-cnpj">CNPJ.BIZ</a>

            <p class="desc">🌐 Diagnóstico e Busca:</p>
            <a href="https://www.google.com" target="_blank" class="btn btn-google">GOOGLE SEARCH</a>
        </div>
        
        <p style="margin-top: 15px; font-size: 0.65rem; color: #484f58;">Sistema Operacional Ghost | Versão 2.0</p>
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
