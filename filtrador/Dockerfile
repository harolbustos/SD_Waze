FROM python:3.12-slim
LABEL authors="harol"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "normalizador.py"]