FROM python:3.13.3-slim

WORKDIR /app

RUN apt update && apt install -y \ 
    libpq-dev \ 
    libgtk-3-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    && apt clean
    
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]