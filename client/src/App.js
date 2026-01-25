import React, { useState, useEffect, useContext } from 'react';
import './App.css';
import { API_BASE_URL } from './config';
import { ThemeProvider, ThemeContext } from './context/ThemeContext';

// Import Components
import CalculatorCard from './components/CalculatorCard';
import UtilityCard from './components/UtilityCard';
import ParityCard from './components/ParityCard';
import StringCard from './components/StringCard';
import ListCard from './components/ListCard';
import EchoCard from './components/EchoCard';

function Dashboard() {
  const [health, setHealth] = useState(null);
  const { theme, toggleTheme } = useContext(ThemeContext);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/health`)
      .then(res => res.json())
      .then(data => setHealth(data))
      .catch(() => setHealth({ status: 'down' }));
  }, []);

  return (
    <div className="app-container">
      <header>
        <div>
          <h1>CI/CD Learning Project</h1>
          <p style={{ margin: 0, opacity: 0.7 }}>React Frontend for Flask API</p>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          {/* Theme Toggle Button */}
          <button className="theme-toggle" onClick={toggleTheme}>
            {theme === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode'}
          </button>

          {/* Status Badge */}
          <div className={`status-badge ${health?.status === 'healthy' ? 'healthy' : 'down'}`}>
            {health?.status === 'healthy' ? '● System Operational' : '● System Down'}
          </div>
        </div>
      </header>

      <div className="dashboard-grid">
        <CalculatorCard />
        <UtilityCard />
        <ParityCard />
        <StringCard />
        <ListCard />
        <EchoCard />
      </div>
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <Dashboard />
    </ThemeProvider>
  );
}

export default App;