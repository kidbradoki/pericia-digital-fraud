import requests
import re
from flask import Flask, render_template_string, request

app = Flask(__name__)

# --- LAYOUT TÁTICO GHOST v7.0 (APROVADO) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>GHOST INTEL v7.0</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            background-color: #000; color: #00FF41; 
            font-family: 'Courier New', monospace; min-height: 100vh;
            display: flex; flex-direction: column; align-items: center;
        }
        #matrix-canvas { position: fixed; top: 0; left: 0; z-index: -1; }
        
        .app-container { width: 95%; max-width: 500px; padding: 25px 10px; display: flex; flex-direction: column; gap: 15px; }
        
        h2 { font-size: 1.2rem; text-align: center; text-shadow: 0 0 10px #00FF41; letter-spacing: 3px; margin-bottom: 5px; }
        
        .module { 
            border: 1px solid #145e1a; border-radius: 12px; padding: 18px; 
            background: rgba(0, 0, 0, 0.85); box-shadow: 0 0 20px rgba(0, 255, 65, 0.15);
        }
        
        h3 { font-size: 0.55rem; color: #00FF41; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.8; }

        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }

        .btn { 
            display: flex; align-items: center; justify-content: center;
            background-color: #00FF41; color: #000; font-weight: 900; 
            border: none; border-radius: 8px; padding: 16px 2px;
            cursor: pointer; font-size: 0.55rem; text-decoration: none; text-transform: uppercase;
            text-align: center; transition: 0.2s; box-shadow: 0 4px #008F11;
        }
        .btn:active { transform: translateY(2px); box-shadow: 0 2px #008F11; }

        .hidden-engine { display: none; margin-top: 15px; padding-top: 10px; border-top: 1px dashed #145e1a; }
        
        input[type="text"], input[type="file"] { 
            width: 100%; padding: 12px; background: #000; border: 1px solid #00FF41; 
            color: #00FF41; border-radius: 5px; font-size: 0.8rem; margin-bottom: 8px; outline: none;
        }

        .status-badge { 
            margin-top: 10px; padding: 12px; border-radius: 6px; 
            background: rgba(0, 255, 65, 0.1); border: 1px solid #00FF41; 
            font-size: 0.65rem; color: #00FF41; line-height: 1.4;
        }
    </style>
</head>
<body>
    <canvas id="matrix-canvas"></canvas>
    <div class="app-container">
        <h2>CENTRAL GHOST v7.0</h2>
        
        <div class="module">
            <h3>MOD 01: BUSCA EXTERNA</h3>
            <div class="grid-3">
                <a href="https://epieos.com" target="_blank" class="btn">EPIEOS</a>
                <a href="https://intelx.io" target="_blank" class="btn">INTELX</a>
                <a href="https://www.social-searcher.com" target="_blank" class="btn">SOCIAL</a>
            </div>
        </div>

        <div class="module">
            <h3>MOD 02: INFRAESTRUTURA</h3>
            <div class="grid-3">
                <a href="https://www.ipqualityscore.com/" target="_blank" class="btn">IP SCAN</a>
                <a href="https://cnpj.biz" target="_blank" class="btn">CNPJ</a>
                <a href="https://shodan.io" target="_blank" class="btn">SHODAN</a>
            </div>
        </div>

        <div class="module">
            <h3>MOD 03: INVESTIGAÇÃO</h3>
            <div class="grid-3">
                <a href="https://www.google.com" target="_blank" class="btn">GOOGLE</a>
                <button onclick="toggleEngine('p-engine')" class="btn">PLACAS</button>
                <button onclick="toggleEngine('u-engine')" class="btn">URL SCAN</button>
            </div>
            <div id="p-engine" class="hidden-engine" style="display:{% if u %}block{% else %}none{% endif %};">
                <form action="/puxar_placa" method="post">
                    <input type="text" name="placa" required>
                    <button class="btn" style="width:100%;">EXECUTAR BUSCA</button>
                </form>
                {% if u %}<div class="status-badge">{{ u.msg }}</div>{% endif %}
            </div>
            <div id="u-engine" class="hidden-engine">
                <form action="/scan_url" method="post">
                    <input type="text" name="url" required>
                    <button class="btn" style="width:100%;">SCANNER</button>
                </form>
            </div>
        </div>

        <div class="module">
            <h3>MOD 04: PERÍCIA DIGITAL</h3>
            <div class="grid-3">
                <button onclick="toggleEngine('f-engine')" class="btn">ARQUIVO</button>
                <button onclick="toggleEngine('f-engine')" class="btn">EXECUTAR</button>
                <a href="/" class="btn">LIMPAR</a>
            </div>
            <div id="f-engine" class="hidden-engine">
                <form action="/analisar" method="post" enctype="multipart/form-data">
                    <input type="file" name="file" required>
                    <button type="submit" class="btn" style="width:100%;">PROCESSAR</button>
                </form>
            </div>
        </div>
    </div>

    <script>
        function toggleEngine(id) {
            const el = document.getElementById(id);
            el.style.display = (el.style.display === 'block') ? 'none' : 'block';
        }

        const canvas = document.getElementById('matrix-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        const fontSize = 16;
        const drops = Array(Math.floor(canvas.width / fontSize)).fill(1);
        function draw() {
            ctx.fillStyle = "rgba(0, 0, 0, 0.1)"; ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = "#00FF41"; ctx.font = fontSize + "px monospace";
            drops.forEach((y, i) => {
                const text = String.fromCharCode(0x30A0 + Math.random() * 96);
                ctx.fillText(text, i * fontSize, y * fontSize);
                if (y * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            });
        }
        setInterval(draw, 35);
    </script>
</body>
</html>
"""

# --- LÓGICA DE EXTRAÇÃO INTERNA ---
@app.route('/')
def index():
    return render_template_string(HTML_PAGE)

@app.route('/puxar_placa', methods=['POST'])
def puxar_placa():
    placa_raw = request.form.get('placa').strip().upper().replace("-", "")
    url = f"https://www.keplaca.com/busca-placa/{placa_raw}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
        
        # Filtros de extração tática
        modelo = re.search(r'Modelo:</th><td><b>(.*?)</b>', html)
        cor = re.search(r'Cor:</th><td><b>(.*?)</b>', html)
        ano = re.search(r'Ano:</th><td><b>(.*?)</b>', html)
        cidade = re.search(r'Cidade:</th><td><b>(.*?)</b>', html)

        if modelo:
            resultado = f"📦 {modelo.group(1)} | 🎨 {cor.group(1) if cor else 'N/I'} | 📅 {ano.group(1) if ano else 'N/I'} | 📍 {cidade.group(1) if cidade else 'N/I'}"
        else:
            resultado = "⚠️ PLACA NÃO ENCONTRADA NA BASE PÚBLICA."
            
    except Exception as e:
        resultado = "❌ ERRO DE CONEXÃO COM O SERVIDOR DE PLACAS."

    return render_template_string(HTML_PAGE, u={'msg': resultado})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
