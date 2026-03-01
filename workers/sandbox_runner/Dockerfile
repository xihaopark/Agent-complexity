FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    docker.io \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir -e .

CMD ["python", "-m", "workers.sandbox_runner.main"]
