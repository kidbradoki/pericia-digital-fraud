import os
from flask import Flask, render_template_string

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        * { box-sizing: border-box; }
        body { background: #0d1117; color: white; font-family: sans-serif; padding: 20px; text-align: center; }
        .box { border: 2px solid #2ea043; padding: 20px; border-radius: 10px; margin-top: 20px; background: #161b22; }
        .btn { 
            display: block; 
            width: 100%; 
            padding: 15px; 
            margin-top: 15px; 
            border-radius: 8px; 
            color: white; 
            text-decoration: none; 
            font-weight: bold; 
        }
        .btn-neoral { background: #238636; } /* Verde */
        .btn-teste { background: #1f6feb; }  /* Azul */
    </style>
</head>
<body>
    <h1>Teste de Conectividade</h1>
    <div class="box">
        <p>Se o site carregar esta tela, o Render está OK.</p>
        
        <a href="https://osint.neoral.com" target="_blank" class="btn btn-neoral">ABRIR NEORAL</a>
        
        <a href="https://www.google.com" target="_blank" class="btn btn-teste">TESTAR CONEXÃO (GOOGLE)</a>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    # Força a porta que o Render costuma usar se a variável falhar
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
