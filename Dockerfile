FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y libgl1
COPY . .
ENV PORT=8080
CMD gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
