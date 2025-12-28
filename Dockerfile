# Use an official Python runtime as a parent image
FROM python:3.12-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"

# Create and activate a virtual environment
RUN python -m venv /opt/venv

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory to your Django project folder
WORKDIR /app/APPOINTMENT-BOOKING-API/appointment_api

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project
COPY . /app/

# Create a script to run migrations and start the server
RUN printf '#!/bin/bash\n' > /app/runner.sh && \
    printf 'cd /app/APPOINTMENT-BOOKING-API/appointment_api\n' >> /app/runner.sh && \
    printf 'python manage.py migrate --noinput\n' >> /app/runner.sh && \
    printf 'gunicorn appointment_api.wsgi:application --bind 0.0.0.0:${PORT:-8000}\n' >> /app/runner.sh

RUN chmod +x /app/runner.sh

# Command to run the application
CMD ["/app/runner.sh"]