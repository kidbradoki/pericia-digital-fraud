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
        body { background-color: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 20px; text-align: center; }
        .container { max-width: 450px; margin: 0 auto; }
        .logo-box {
            width: 140px; height: 140px; margin: 0 auto 20px;
            border-radius: 50%; border: 3px solid #2ea043;
            overflow: hidden; box-shadow: 0 0 20px rgba(46, 160, 67, 0.4);
            background-color: #161b22;
        }
        .logo-box img { width: 100%; height: 100%; object-fit: cover; }
        .box { border: 2px solid #30363d; border-radius: 12px; padding: 15px; background: #161b22; text-align: left; }
        .btn {
            display: block; width: 100%; padding: 14px; text-decoration: none;
            border-radius: 8px; font-weight: bold; margin-top: 10px;
            text-align: center; color: white; font-size: 0.9rem;
        }
        .btn-epieos { background-color: #238636; }
        .btn-intelx { background-color: #8957e5; }
        .btn-social { background-color: #d29922; }
        .btn-ip { background-color: #f85149; }
        .btn-cnpj { background-color: #0969da; }
        .btn-google { background-color: #30363d; border: 1px solid #8b949e; }
        h2 { color: #3fb950; margin-bottom: 5px; font-size: 1.3rem; }
        .label { font-size: 0.75rem; color: #8b949e; margin-top: 10px; font-weight: bold; display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo-box">
            <img src="https://raw.githubusercontent.com/kidbradoki/pericia-digital-fraud/main/OSINT.jpg" alt="Ghost Logo">
        </div>
        <h2>Painel de Perícia</h2>
        <p style="font-size: 0.8rem; margin-bottom: 15px;">[ STATUS: OPERACIONAL ]</p>
        <div class="box">
            <span class="label">IDENTIDADE & EMAIL:</span>
            <a href="https://epieos.com" target="_blank" class="btn btn-epieos">EPIEOS</a>
            <span class="label">VAZAMENTOS & DEEP WEB:</span>
            <a href="https://intelx.io" target="_blank" class="btn btn-intelx">INTELX</a>
            <span class="label">REDES SOCIAIS:</span>
            <a href="https://www.social-searcher.com" target="_blank" class="btn btn-social">SOCIAL SEARCHER</a>
            <span class="label">IP & GEOLOCALIZAÇÃO:</span>
            <a href="https://ip-api.com" target="_blank" class="btn btn-ip">IP-API</a>
            <span class="label">EMPRESAS & SOCIEDADE:</span>
            <a href="https://cnpj.biz" target="_blank" class="btn btn-cnpj">CNPJ.BIZ</a>
            <span class="label">DIAGNÓSTICO:</span>
            <a href="https://www.google.com" target="_blank" class="btn btn-google">GOOGLE SEARCH</a>
        </div>
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
