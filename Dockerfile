# Use Python 3.9 image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files for WhiteNoise
RUN python manage.py collectstatic --noinput --clear

# Expose port 8000 (Django default)
EXPOSE 8000

# Run Gunicorn with environment variable for port
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT:-8000}", "multiverseclothing.wsgi:application"]
