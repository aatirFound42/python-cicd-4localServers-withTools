# ============= BUILDER STAGE =============
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies
RUN npm install --production

# Copy application source code
COPY public/ ./public/
COPY src/ ./src/

# Build the React app for production
# Use relative path for API - nginx will proxy it
RUN npm run build

# ============= RUNTIME STAGE =============
FROM nginx:alpine

# Metadata labels
LABEL description="React frontend for Python CI/CD learning project"

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Create custom nginx config with API proxy
RUN cat > /etc/nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name _;
    
    # Frontend static files
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
    
    # Proxy /api requests to backend
    location /api {
        # Use Docker DNS to resolve backend container
        resolver 127.0.0.11 valid=30s;
        set $backend cicd-backend;
        proxy_pass http://$backend:5000;
        
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 10s;
        proxy_send_timeout 10s;
        proxy_read_timeout 10s;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PUT, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type, Authorization' always;
        
        # Handle preflight OPTIONS requests
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
}
EOF

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Expose port 80
EXPOSE 80

# Start Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]