from flask import Flask, render_template_string

app = Flask(__name__)

# Seu HTML completo e corrigido aqui dentro
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
            overflow-x: hidden; 
            padding: 15px;
        }
        .ferramenta-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            width: 100%;
        }
        .dossie-box {
            border: 2px solid #2ea043;
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            background: #0d1117;
            word-wrap: break-word; /* CORRIGE AS LINHAS VERDES VAZANDO */
            overflow-wrap: break-word;
        }
        .link-click {
            color: #58a6ff;
            text-decoration: underline;
            font-weight: bold;
            word-break: break-all;
        }
        .btn-analise {
            background-color: #238636;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            width: 100%;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <h1>Central de Perícia Digital</h1>
    <div class="ferramenta-card">
        <h3>🔍 Rastreio OSINT</h3>
        <button class="btn-analise">INICIAR ANÁLISE</button>
        <div class="dossie-box">
            <p style="color:#3fb950; text-align:center;"><b>DOSSIÊ DE FONTES ABERTAS</b></p>
            <p>✅ ALVO: kidbradoki@gmail.com</p>
            <br>
            <p>🌐 <b>LINK CLICÁVEL:</b></p>
            <a href="https://osint.neoral.com" target="_blank" class="link-click">https://osint.neoral.com</a>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
