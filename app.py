<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Central de Perícia Digital</title>
    <style>
        /* MANTENDO SEU DESIGN DARK E CORRIGINDO PROPORÇÃO */
        * {
            box-sizing: border-box; 
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            overflow-x: hidden; /* Evita que o site "dance" para os lados */
            width: 100vw;
            padding: 15px;
        }

        h1 {
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 20px;
            color: #ffffff;
        }

        /* CARD DE CADA FERRAMENTA */
        .ferramenta-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            width: 100%; /* Garante que ocupe a tela toda sem vazar */
        }

        /* O QUE VOCÊ CHAMA DE 'LINHAS VERDES' (DOSSIÊ) */
        .dossie-box {
            border: 2px solid #2ea043; /* O contorno verde que você quer */
            border-radius: 8px;
            padding: 10px;
            margin-top: 15px;
            background: #0d1117;
            word-wrap: break-word; /* FORÇA O TEXTO A QUEBRAR A LINHA */
            overflow-wrap: break-word;
            font-family: monospace; /* Estilo hacker/investigação */
            font-size: 0.9rem;
        }

        .titulo-verde {
            color: #3fb950;
            font-weight: bold;
            text-align: center;
            margin-bottom: 10px;
            text-transform: uppercase;
            border-bottom: 1px solid #2ea043;
            padding-bottom: 5px;
        }

        /* LINK CLICÁVEL DO OSINT NEORAL */
        .link-click {
            color: #58a6ff;
            text-decoration: underline;
            font-weight: bold;
            display: inline-block;
            margin-top: 10px;
            word-break: break-all;
        }

        .link-click:hover {
            color: #1f6feb;
        }

        /* BOTÃO INICIAR ANÁLISE */
        .btn-analise {
            background-color: #238636;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            width: 100%;
            font-weight: bold;
            cursor: pointer;
            margin-top: 10px;
        }

        input[type="text"], input[type="email"] {
            width: 100%;
            padding: 10px;
            background: #0d1117;
            border: 1px solid #30363d;
            color: white;
            border-radius: 6px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>

    <h1>Central de Perícia Digital</h1>

    <div class="ferramenta-card">
        <h3>🔍 Rastreio OSINT</h3>
        <p style="font-size: 0.8rem; margin-bottom: 10px; color: #8b949e;">
            Insira o @usuario ou e-mail para rastrear pegadas digitais.
        </p>
        
        <input type="text" placeholder="Insira os dados para perícia...">
        <button class="btn-analise">INICIAR ANÁLISE</button>

        <div class="dossie-box">
            <div class="titulo-verde">Dossiê de Fontes Abertas</div>
            <p>✅ <strong>ALVO:</strong> kidbradoki@gmail.com</p>
            <p>🔎 <strong>VARREDURA:</strong> Bases Públicas</p>
            <br>
            <p>🌐 <strong>LINK PARA RELATÓRIO:</strong></p>
            <a href="https://osint.neoral.com" target="_blank" class="link-click">
                https://osint.neoral.com
            </a>
            <br><br>
            <p style="font-size: 0.7rem; color: #8b949e;">LOG: 06/05/2026 01:56:06</p>
        </div>
    </div>

    </body>
</html>
