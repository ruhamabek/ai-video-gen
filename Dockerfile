# Dockerfile for The Heritage Short Film Pipeline
# Guaranteed reproducible studio container with full FFmpeg, libx264, and Python runtime

FROM python:3.11-slim

# Prevent Python from writing bytecode and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies: FFmpeg (with libx264 and subtitles/libass support), git, make, fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    fonts-dejavu-core \
    fonts-liberation \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements / project definition and install dependencies
COPY pyproject.toml .python-version ./
RUN pip install --no-cache-dir jsonschema python-dotenv pillow

# Copy pipeline source code, schema, and storyboard contract
COPY pipeline/ ./pipeline/
COPY schema/ ./schema/
COPY storyboard.json ./
COPY SCRIPT.md ./
COPY Makefile ./

# Create default outputs mount point
RUN mkdir -p outputs

# Default entrypoint: Run the full film pipeline end-to-end
CMD ["python", "-m", "pipeline.orchestrate"]
