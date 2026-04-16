FROM python:3.10-slim

WORKDIR /app

# Runtime prerequisites for workflow engines (installed on demand)
RUN apt-get update && apt-get install -y --no-install-recommends \
    bash \
    ca-certificates \
    curl \
    git \
    default-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Install Docker CLI binary (no host /usr/bin/docker bind required).
RUN set -eux; \
    arch="$(uname -m)"; \
    case "$arch" in \
      x86_64) docker_arch="x86_64" ;; \
      aarch64) docker_arch="aarch64" ;; \
      *) echo "Unsupported architecture: $arch" && exit 1 ;; \
    esac; \
    docker_cli_version="29.2.1"; \
    curl -fsSL "https://download.docker.com/linux/static/stable/${docker_arch}/docker-${docker_cli_version}.tgz" -o /tmp/docker.tgz; \
    tar -xzf /tmp/docker.tgz -C /tmp; \
    mv /tmp/docker/docker /usr/local/bin/docker; \
    chmod +x /usr/local/bin/docker; \
    rm -rf /tmp/docker /tmp/docker.tgz

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY api_gateway.py .
COPY controller_events.py .

# Create data directories
RUN mkdir -p /app/data/uploads /app/data/artifacts /app/data/workflows

EXPOSE 18000

CMD ["uvicorn", "api_gateway:app", "--host", "0.0.0.0", "--port", "18000"]
