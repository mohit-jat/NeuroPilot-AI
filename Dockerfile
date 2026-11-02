FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment settings
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV PYTHONUNBUFFERED=1

# Expose FastAPI (8000) and Gradio (7860)
EXPOSE 8000 7860

# Run both Backend & Frontend
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & python frontend/app.py"]
