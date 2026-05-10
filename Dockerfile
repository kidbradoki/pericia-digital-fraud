# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Evita que o Python gere arquivos .pyc e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do SISTEMA (O motor que faltava para o OCR e Imagens)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia primeiro apenas o requirements para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos do seu projeto (app.py, etc)
COPY . .

# Expõe a porta padrão do Hugging Face Spaces
EXPOSE 7860

# Comando para iniciar o servidor usando o Gunicorn (Próprio para produção)
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
