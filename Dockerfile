# Multi-stage build for Cyfox
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    nmap \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY cyfox/ ./cyfox/
COPY config/ ./config/
COPY frontend/assets/ ./frontend/assets/
COPY run.py .

# Create non-root user for security
RUN useradd -m -u 1000 cyfox && \
    chown -R cyfox:cyfox /app

USER cyfox

# Expose any necessary ports (if web interface added later)
# EXPOSE 8080

# Run the application
CMD ["python", "run.py"]

