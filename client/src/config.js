// // This will be replaced at build time
// export const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

// Use relative path - nginx will proxy to backend
// export const API_BASE_URL = "/api";  // Changed from http://cicd-backend:5000

// For development, use localhost
// For production, use relative path (nginx proxies)
export const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // Nginx will proxy this
  : 'http://localhost:5000/api';  // Direct connection in dev