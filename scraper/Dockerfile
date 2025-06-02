FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget curl unzip gnupg ca-certificates fonts-liberation libnss3 libatk1.0-0 \
    libatk-bridge2.0-0 libxcomposite1 libxrandr2 libgbm1 libgtk-3-0 libxdamage1 \
    libxfixes3 libxrender1 libasound2 libxtst6 xauth xvfb libxshmfence-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements .
RUN pip install --no-cache-dir -r requirements

RUN pip install playwright && playwright install chromium

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "scraper.py"]
