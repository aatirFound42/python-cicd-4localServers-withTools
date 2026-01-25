# Multi-stage Docker build for React CI/CD application
# Stage 1: Builder - Install dependencies and build the app
# Stage 2: Runtime - Serve with Nginx

# ============= BUILDER STAGE =============
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --production

# Copy application source code
COPY public/ ./public/
COPY src/ ./src/

# Build the React app for production
# This creates an optimized build in /app/build
RUN npm run build

# ============= RUNTIME STAGE =============
FROM nginx:alpine

# Metadata labels
LABEL description="React frontend for Python CI/CD learning project"

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Create non-root user for better security
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser && \
    chown -R appuser:appuser /usr/share/nginx/html && \
    chown -R appuser:appuser /var/cache/nginx && \
    chown -R appuser:appuser /var/log/nginx && \
    touch /var/run/nginx.pid && \
    chown -R appuser:appuser /var/run/nginx.pid

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Expose port 80
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]