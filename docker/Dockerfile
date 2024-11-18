# Stage 1: Base image with necessary dependencies
FROM python:3.11-slim as base

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (required for PostgreSQL, MongoDB, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libssl-dev \
    libsasl2-dev \
    python-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Install Python dependencies in a clean image
FROM base as builder

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final image for production
FROM base

# Copy installed dependencies and the application code from the builder stage
COPY --from=builder /app /app

# Expose the application port
EXPOSE 8000

# Set environment variables (for example, to configure logging, database URL)
ENV DATABASE_URL=postgresql://user:password@postgres:5432/healthsphere
ENV MONGO_URI=mongodb://mongo:27017/healthsphere

# Command to run the FastAPI app with uvicorn (ASGI server)
CMD ["uvicorn", "healthapp.main:app", "--host", "0.0.0.0", "--port", "8000"]
