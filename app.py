import requests, re, os
from flask import Flask, render_template_string, request
from PIL import Image
from PIL.ExifTags import TAGS
import pytesseract
import PyPDF2

# --- CONFIGURAÇÃO DE AMBIENTE HUGGING FACE ---
# Define o caminho do executável do Tesseract no Linux do Space
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
# ---------------------------------------------

app = Flask(__name__)

# Interface Visual GHOST v8.6 - Estilo Matrix/Terminal
H = """
<!DOCTYPE html><html lang="pt-br"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no"><title>GHOST v8.6</title><style>
*{box-sizing:border-box;margin:0;padding:0}body{background:#000;color:#00FF41;font-family:monospace;min-height:100vh;display:flex;flex-direction:column;align-items:center}#m{position:fixed;top:0;left:0;z-index:-1}.app{width:95%;max-width:500px;padding:25px 10px;display:flex;flex-direction:column;gap:15px}h2{font-size:1.2rem;text-align:center;text-shadow:0 0 10px #00FF41;letter-spacing:3px}.mod{border:1px solid #145e1a;border-radius:12px;padding:18px;background:rgba(0,0,0,0.85);box-shadow:0 0 20px rgba(0,255,65,0.15)}h3{font-size:0.55rem;margin-bottom:12px;text-transform:uppercase;opacity:0.8}.g3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.btn{display:flex;align-items:center;justify-content:center;background:#00FF41;color:#000;font-weight:900;border:none;border-radius:8px;padding:16px 2px;cursor:pointer;font-size:0.55rem;text-transform:uppercase;box-shadow:0 4px #008F11;text-decoration:none}.btn:active{transform:translateY(2px);box-shadow:0 2px #008F11}.eng{display:none;margin-top:15px;padding-top:10px;border-top:1px dashed #145e1a}input{width:100%;padding:12px;background:#000;border:1px solid #00FF41;color:#00FF41;border-radius:5px;margin-bottom:8px;outline:none}.res{margin-top:10px;padding:12px;border-radius:6px;background:rgba(0,255,65,0.1);border:1px solid #00FF41;font-size:0.65rem;word-break:break-all;max-height:300px;overflow-y:auto;}.warn{color:#FF4141;font-weight:bold;display:block;margin-bottom:5px;text-transform:uppercase;}
</style></head><body><canvas id="m"></canvas><div class="app"><h2>CENTRAL GHOST v8.6</h2>
<div class="mod"><h3>MOD 01: OSINT</h3><div class="g3"><a href="https://epieos.com" target="_blank" class="btn">EPIEOS</a><a href="https://intelx.io" target="_blank" class="btn">INTELX</a><a href="https://www.social-searcher.com" target="_blank" class="btn">SOCIAL</a></div></div>
<div class="mod"><h3>MOD 02: TÉCNICO</h3><div class="g3"><a href="https://ipqualityscore.com/" target="_blank" class="btn">IP SCAN</a><a href="https://cnpj.biz" target="_blank" class="btn">CNPJ</a><a href="https://shodan.io" target="_blank" class="btn">SHODAN</a></div></div>
<div class="mod"><h3>MOD 03: INVESTIGAÇÃO</h3><div class="g3"><a href="https://google.com" target="_blank" class="btn">GOOGLE</a><button onclick="t('pe')" class="btn">PLACAS</button><button onclick="t('ue')" class="btn">URL SCAN</button></div>
<div id="pe" class="eng" style="display:{% if mp %}block{% else %}none{% endif %};"><form action="/p" method="post"><input type="text" name="placa" placeholder="DIGITE A PLACA" required><button class="btn" style="width:100%">EXECUTAR</button></form>{% if mp %}<div class="res">{{ mp }}</div>{% endif %}</div>
<div id="ue" class="eng" style="display:{% if ms %}block{% else %}none{% endif %};"><form action="/s" method="post"><input type="text" name="url" placeholder="URL PARA SCAN" required><button class="btn" style="width:100%">SCANNER</button></form>{% if ms %}<div class="res">{{ ms }}</div>{% endif %}</div></div>
<div class="mod"><h3>MOD 04: PERÍCIA</h3><div class="g3"><button onclick="t('fe')" class="btn">ARQUIVO</button><button onclick="t('fe')" class="btn">ANALISAR</button><a href="/" class="btn">LIMPAR</a></div>
<div id="fe" class="eng" style="display:{% if ma %}block{% else %}none{% endif %};"><form action="/a" method="post" enctype="multipart/form-data"><input type="file" name="file" required><button class="btn" style="width:100%">PROCESSAR ALVO</button></form>{% if ma %}<div class="res">{{ ma|safe }}</div>{% endif %}</div></div></div>
<script>function t(id){let e=document.getElementById(id);e.style.display=(e.style.display==='block')?'none':'block'}const c=document.getElementById('m'),x=c.getContext('2d');c.width=window.innerWidth;c.height=window.innerHeight;const f=16,d=Array(Math.floor(c.width/f)).fill(1);function draw(){x.fillStyle="rgba(0,0,0,0.1)";x.fillRect(0,0,c.width,c.height);x.fillStyle="#00FF41";x.font=f+"px monospace";d.forEach((y,i)=>{const t=String.fromCharCode(0x30A0+Math.random()*96);x.fillText(t,i*f,y*f);if(y*f>c.height&&Math.random()>0.975)d[i]=0;d[i]++});}setInterval(draw,35);</script></body></html>
"""

@app.route('/')
def index(): return render_template_string(H)

@app.route('/p', methods=['POST'])
def p():
    pl = request.form.get('placa', '').strip().upper().replace("-","")
    try:
        r = requests.get(f"https://www.keplaca.com/busca-placa/{pl}", timeout=10).text
        m = re.search(r'Modelo:</th><td><b>(.*?)</b>', r); c = re.search(r'Cor:</th><td><b>(.*?)</b>', r)
        res = f"📦 {m.group(1)} | 🎨 {c.group(1) if c else 'N/I'}" if m else "⚠️ PLACA NÃO LOCALIZADA."
    except: res = "❌ ERRO NA CONSULTA."
    return render_template_string(H, mp=res)

@app.route('/s', methods=['POST'])
def s():
    u = request.form.get('url', '')
    return render_template_string(H, ms=f"🔎 URL REGISTRADA PARA MONITORAMENTO: {u}")

@app.route('/a', methods=['POST'])
def a():
    f = request.files.get('file'); res = ""; alert = ""
    if not f: return render_template_string(H, ma="⚠️ NENHUM ARQUIVO PARA ANÁLISE.")
    ext = f.filename.split('.')[-1].lower()
    try:
        if ext in ['jpg', 'jpeg', 'png']:
            img = Image.open(f)
            # OCR em Português
            txt = pytesseract.image_to_string(img, lang='por').upper()
            # Extração EXIF
            ex = img._getexif()
            meta = " | ".join([f"{TAGS.get(k,k)}:{v}" for k,v in ex.items() if isinstance(v,(str,int))][:5]) if ex else "SEM METADADOS (REMOVIDOS)"
            
            # Verificação de manipuladores
            f_words = ["CANVA", "PHOTOSHOP", "PICSART", "EDIT", "ADOBE", "INSTAGRAM"]
            if any(x in meta.upper() or x in txt for x in f_words):
                alert = "<span class='warn'>[!] ALERTA: INDICADORES DE MANIPULAÇÃO ENCONTRADOS</span>"
            
            res = f"{alert}🔍 <b>META:</b> {meta}<br><br>📝 <b>LEITURA OCR:</b><br>{txt[:350]}"

        elif ext == 'pdf':
            pdf = PyPDF2.PdfReader(f)
            info = pdf.metadata
            d = " | ".join([f"{k[1:]}:{v}" for k,v in info.items() if isinstance(v, str)][:5]) if info else "DADOS ESTRUTURAIS AUSENTES"
            
            if any(x in d.upper() for x in ["CANVA", "EDITOR", "ILLUSTRATOR", "ILOVEPDF"]):
                alert = "<span class='warn'>[!] ALERTA: PDF GERADO POR SOFTWARE DE TERCEIROS</span>"
            
            res = f"{alert}📄 <b>PROPRIEDADES:</b> {d}<br>📊 <b>PÁGINAS:</b> {len(pdf.pages)}"
        else:
            res = "⚠️ FORMATO NÃO SUPORTADO."
    except Exception as e:
        res = f"❌ FALHA NO MOTOR DE PERÍCIA: {str(e)}"
    
    return render_template_string(H, ma=f"📄 ALVO: {f.filename}<br>{res}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)
