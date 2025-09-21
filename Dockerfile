# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (Railway uses PORT environment variable)
EXPOSE $PORT

# Run the application with dynamic port
CMD python -m uvicorn api:app --host 0.0.0.0 --port $PORT