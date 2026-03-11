# Base image
FROM python:3.10.12

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first (Docker cache optimization)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY src/ src/
COPY data/ data/
COPY results/ results/
COPY run_pipeline.sh .

# Make script executable
RUN chmod +x run_pipeline.sh

# Create non-root user (good practice)
RUN useradd -m researcher
USER researcher

# Default command
CMD ["./run_pipeline.sh"]
