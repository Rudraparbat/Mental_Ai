# Use slim image for a smaller footprint
FROM python:3.13.2-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    pkg-config \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app


# Copy the rest of the application
COPY . .

RUN pip install --no-cache-dir -r requirements.txt  

RUN pip uninstall -y pinecone-plugin-inference

RUN chmod +x /app/entrypoint.sh
# Set environment variables
ENV DJANGO_SETTINGS_MODULE=mental.settings
ENV PYTHONUNBUFFERED=1

# Expose the application port
EXPOSE 8000

# Use proper ENTRYPOINT syntax
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
