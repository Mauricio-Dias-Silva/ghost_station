FROM python:3.11-slim

WORKDIR /app

# Instala a libgl1 (Correção para o erro de imagem)
RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8080

# CONFIRA SE A PASTA É 'config' MESMO. SE FOR OUTRA, TROQUE O NOME AQUI:
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
