import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Layout Blindado com Ferramentas Ativas
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
            margin-top: 12px;
            text-align: center;
            border: none;
            color: white;
        }

        /* Cores das Ferramentas Ativas */
        .btn-epieos { background-color: #238636; } /* Verde - E-mails */
        .btn-intelx { background-color: #8957e5; } /* Roxo - Vazamentos */
        .btn-social { background-color: #d29922; } /* Laranja - Redes Sociais (Alternativa ao Sherlock) */
        .btn-google { background-color: #1f6feb; } /* Azul - Busca/Diagnóstico */
        
        h2 { margin-bottom: 10px; font-size: 1.4rem; }
        .desc { font-size: 0.85rem; color: #8b949e; margin-bottom: 5px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Painel de Perícia Digital</h2>
        <p style="font-size: 0.8rem; color: #3fb950;">[ GHOST - SISTEMA OPERACIONAL ]</p>
        
        <div class="box">
            <p class="desc">🔎 Busca por E-mail e Identidade:</p>
            <a href="https://epieos.com" target="_blank" class="btn btn-epieos">ABRIR EPIEOS</a>

            <p class="desc">🗄️ Vazamentos e Dados Históricos:</p>
            <a href="https://intelx.io" target="_blank" class="btn btn-intelx">ABRIR INTELX</a>

            <p class="desc">📱 Monitoramento de Redes Sociais:</p>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-social">ABRIR SOCIAL-SEARCHER</a>

            <p class="desc">🌐 Busca Manual e Diagnóstico:</p>
            <a href="https://www.google.com" target="_blank" class="btn btn-google">BUSCA NO GOOGLE</a>
        </div>
        
        <p style="margin-top: 15px; font-size: 0.7rem; color: #484f58;">Status: Servidor Render Live | Porta 10000</p>
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
