FROM python:3.11-slim

WORKDIR /app

# Cài đặt dependencies cần thiết
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements trước để tận dụng Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Cài đặt matplotlib và các dependencies khác
RUN pip install --no-cache-dir matplotlib pandas numpy

# Copy toàn bộ code
COPY . .

# Tạo thư mục cho logs và cache
RUN mkdir -p /app/logs /app/cache

# Set permissions
RUN chmod +x run.py migrate.py split_commands.py

# Expose port (nếu cần)
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:3000/health')" || exit 1

# Default command
CMD ["python", "run.py"]