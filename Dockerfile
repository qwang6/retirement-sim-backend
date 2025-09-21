FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Railway will provide PORT at runtime
EXPOSE 8000

# Use exec form to properly handle environment variables
CMD exec uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}