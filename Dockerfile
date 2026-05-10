FROM python:3.10

# Instala as dependências do sistema (O MOTOR DO OCR)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libtesseract-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Cria o diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Porta do Hugging Face
EXPOSE 7860

# Comando para rodar a Central
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]
