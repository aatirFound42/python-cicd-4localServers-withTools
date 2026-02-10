# Multi-stage Docker build for Python CI/CD application
# Stage 1: Builder - Install dependencies
# Stage 2: Runtime - Run application

# ============= BUILDER STAGE =============
FROM python:3.9-slim AS builder

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies in user directory (no root needed) (creates a layer)
RUN  python -m pip install --upgrade pip
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy application code 
COPY app/ app/
COPY tests/ tests/

# ============= RUNTIME STAGE =============
FROM python:3.9-slim

# Metadata labels
LABEL description="A simple Python CI/CD application using Flask"

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser

# Copy Python dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY app/ ./app/

# Set environment variables
# ENV PATH=/home/appuser/.local/bin:$PATH
ENV FLASK_APP=app/main.py
ENV PYTHONUNBUFFERED=1

# Set ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/', timeout=2)" || exit 1

# Expose port
EXPOSE 5000

# Run Flask application
CMD ["python", "-m", "flask", "run", "--host", "0.0.0.0"]
