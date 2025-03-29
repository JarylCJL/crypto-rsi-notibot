# Use Python 3.10 slim image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set timezone (optional, useful for consistent logs)
ENV TZ=Asia/Singapore

# Entrypoint
CMD ["python", "run_bot.py"]
