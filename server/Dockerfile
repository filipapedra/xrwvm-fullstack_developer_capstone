# Use official Python image
FROM python:3.12.0-slim-bookworm

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONWRITEBYTECODE=1 \
    APP=/app

# Set working directory
WORKDIR $APP

# Copy requirements and install dependencies
COPY requirements.txt $APP/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project files into the container
COPY . $APP/

# Expose port 8000 (default for Django dev server or Gunicorn)
EXPOSE 8000

# Make sure entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# Default entrypoint
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

# Fallback command if none is provided
CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoproj.wsgi"]
