# Usa uma imagem oficial do Python como base
FROM python:3.10-slim

# Evita arquivos temporários e permite logs em tempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependências do SISTEMA (Correção para Debian Trixie/Hugging Face)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    libgl1 \
    libglib2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Instala as bibliotecas do Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Porta do Hugging Face
EXPOSE 7860

# Inicia o servidor
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
