import os
from flask import Flask, render_template_string, request, jsonify
# Mantendo as bibliotecas de peso da V7.0
import torch
import easyocr
import requests

app = Flask(__name__)

# CSS GHOST V7.0 - Otimizado para visual Dark e carregamento fluido
CSS = """
<style>
    body {
        background-color: #0b0d0f; /* Visual Furtivo */
        color: #e0e0e0;
        font-family: 'Segoe UI', Roboto, sans-serif;
        margin: 0;
        padding: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
    }

    .container {
        max-width: 600px;
        width: 100%;
        text-align: center;
    }

    h1 {
        color: #58a6ff;
        font-size: 26px;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 15px rgba(88, 166, 255, 0.4);
    }

    .subtitle {
        color: #8b949e;
        font-size: 12px;
        margin-bottom: 30px;
        letter-spacing: 1px;
    }

    .button-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 15px;
        width: 100%;
    }

    .btn {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #c9d1d9;
        padding: 20px 10px;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .btn:hover {
        background-color: #21262d;
        border-color: #58a6ff;
        color: #58a6ff;
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.6);
    }

    .status-bar {
        margin-top: 30px;
        padding: 10px;
        border-top: 1px solid #30363d;
        width: 100%;
        font-size: 11px;
        color: #484f58;
        display: flex;
        justify-content: space-between;
    }
</style>
"""

HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CENTRAL GHOST V7.0</title>
    {CSS}
</head>
<body>
    <div class="container">
        <h1>GHOST BRAVO V7.0</h1>
        <p class="subtitle">SISTEMA AVANÇADO DE PERÍCIA E OSINT</p>
        
        <div class="button-grid">
            <a href="#" class="btn">EPIEOS SEARCH</a>
            <a href="#" class="btn">INTELX LEAKS</a>
            <a href="#" class="btn">SOCIAL TRACKER</a>
            <a href="#" class="btn">IP NETWORK SCAN</a>
            <a href="#" class="btn">CONSULTA CNPJ</a>
            <a href="#" class="btn">GOOGLE DORKING</a>
            <a href="#" class="btn">OCR ANALYZER</a>
            <a href="#" class="btn">METADATA EXTRACT</a>
        </div>

        <div class="status-bar">
            <span>SISTEMA: OPERACIONAL</span>
            <span>BASE: HUGGING FACE ALPHA</span>
        </div>
    </div>
</body>
</html>
"""

# Mantendo as rotas e a lógica de processamento da V7.0
@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# Aqui continuariam as tuas funções de OCR e Scrapers que já estão no repo
# ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
