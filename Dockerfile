# Dockerfile para projetos com Visão Computacional (OpenCV/Imagem)
FROM python:3.11-slim

# Otimizações
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

WORKDIR /app

# --- A CORREÇÃO MÁGICA ESTÁ AQUI ---
# Instala bibliotecas gráficas do sistema que o 'slim' não tem
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copia o código
COPY . .

# Comando de inicialização
# ATENÇÃO: Confirme se 'config.wsgi' é o nome correto da pasta do seu projeto!
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
