# ====================================================================
# Dockerfile — builds a runnable image of the Documents API.
# Build:  docker build -t documents-api .
# Run:    docker run -p 8000:8000 documents-api
# ====================================================================

# Start from a slim Python 3.11 base image (small download, fewer vulns).
FROM python:3.11-slim

# Set the working directory inside the container.
# All following commands run from here.
WORKDIR /app

# Copy just the requirements file first. Docker caches this layer, so
# if we only change code later, we skip reinstalling dependencies.
COPY requirements.txt .

# Install dependencies. --no-cache-dir keeps the image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the source code into the image.
COPY . .

# Expose port 8000 (informational — also need -p when running).
EXPOSE 8000

# Command that runs when the container starts.
# This is the same command you'd run locally: `python index.py`.
CMD ["python", "index.py"]