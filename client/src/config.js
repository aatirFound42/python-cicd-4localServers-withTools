// API configuration
// This gets replaced at build time via REACT_APP_API_URL environment variable
export const API_BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

// Log the API URL in development for debugging
if (process.env.NODE_ENV === 'development') {
  console.log('API Base URL:', API_BASE_URL);
}