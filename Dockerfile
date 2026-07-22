# Use official Python image
FROM  python:3.14.6-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cach-dir -r requirements.txt