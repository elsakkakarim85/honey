FROM python:3.11-slim

# Install system dependencies for cryptography and audio processing
RUN apt-get update && apt-get install -y \
    build-essential \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend source code
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the Uvicorn server
CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
