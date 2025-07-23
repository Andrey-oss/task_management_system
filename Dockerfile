FROM python:3.11-slim

# Install useful packages and clean APT cache
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add some variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Setup work dir
WORKDIR /app

# Copy all
COPY . .

# Do venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install deps
RUN pip install --upgrade pip && pip install -r requirements.txt

# Open port
EXPOSE 8000

# Apply migrations
RUN python manage.py makemigrations 
RUN python manage.py migrate 

# By default: 127.0.0.1:8000
CMD ["python", "manage.py", "runserver"]