# Use slim image for a smaller footprint
FROM python:3.13-slim-bookworm

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements fir
# Install dependencies


# Copy the rest of the application
COPY . .

RUN pip install --no-cache-dir -r requirements.txt  

RUN chmod +x /app/entrypoint.sh
# Set environment variables
ENV DJANGO_SETTINGS_MODULE=mental.settings
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Use proper ENTRYPOINT syntax
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
