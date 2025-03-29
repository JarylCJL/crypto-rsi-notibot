# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Copy required files into container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip \
 && pip install -r requirements.txt

# Expose port (if needed, not used for Telegram bot)
# EXPOSE 8000

# Default command
CMD ["python", "run_bot.py"]
