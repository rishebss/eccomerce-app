FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps: libpq for psycopg2, libjpeg/zlib for Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (cached layer)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Collect static files (whitenoise). Allow failure if DB not available at build time
RUN python manage.py collectstatic --noinput || echo "collectstatic skipped"

EXPOSE 8000

# Run migrations then start with gunicorn (WSGI)
# Uses $PORT if platform provides it (Koyeb/Render/Railway), else 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn multiverseclothing.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 3 --timeout 120"]
