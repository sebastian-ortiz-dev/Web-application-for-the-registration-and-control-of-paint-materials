FROM python:3.13.3-slim AS builder


RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    libpangocairo-1.0-0 \
    libffi-dev \
    shared-mime-info \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.13.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libpangocairo-1.0-0 \
    libcairo2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --chown=apiuser . .

RUN useradd -ms /bin/bash apiuser
USER apiuser

COPY --chown=apiuser --from=builder /root/.local /home/apiuser/.local

ENV PATH=/home/apiuser/.local/bin:$PATH

CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]