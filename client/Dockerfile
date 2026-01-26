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

# Build argument for API URL - this will be baked into the React build
ARG REACT_APP_API_URL=http://localhost:5000
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Build the React app for production
RUN npm run build

# ============= RUNTIME STAGE =============
FROM nginx:alpine

# Metadata labels
LABEL description="React frontend for Python CI/CD learning project"

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Simple nginx config - just serve static files
RUN cat > /etc/nginx/conf.d/default.conf <<'EOF'
server {
    listen 80;
    server_name _;
    
    # Serve static files
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
        add_header Cache-Control "no-cache, no-store, must-revalidate";
    }
}
EOF

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]