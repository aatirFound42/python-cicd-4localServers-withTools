import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function UtilityCard() {
  const [n, setN] = useState('');
  const [result, setResult] = useState(null);

  const calculate = async (operation) => {
    try {
      const res = await fetch(`${API_BASE_URL}/${operation}?n=${n}`);
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Error fetching data" });
    }
  };

  return (
    <div className="card">
      <h2>🛠️ Utilities</h2>
      <div className="input-group">
        <input type="number" placeholder="Enter Number (n)" value={n} onChange={e => setN(e.target.value)} />
      </div>
      <div className="btn-group">
        <button onClick={() => calculate('square')}>Square (n²)</button>
        <button onClick={() => calculate('abs')}>Absolute |n|</button>
      </div>
      {result && (
        <div className="result-box">
          <strong>Result: {result.result}</strong>
          <div className="json-display">Timestamp: {result.timestamp}</div>
        </div>
      )}
    </div>
  );
}

export default UtilityCard;