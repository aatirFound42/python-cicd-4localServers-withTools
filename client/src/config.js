// API configuration
// Use /api prefix - nginx will proxy to backend
export const API_BASE_URL = "/api";

// Log the API URL in development for debugging
if (process.env.NODE_ENV === 'development') {
  console.log('API Base URL:', API_BASE_URL);
}