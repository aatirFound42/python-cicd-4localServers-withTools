import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function CalculatorCard() {
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [result, setResult] = useState(null);

  const calculate = async (operation) => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/${operation}?a=${a}&b=${b}`);
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Failed to connect to API" });
    }
  };

  return (
    <div className="card">
      <h2>🧮 Calculator</h2>
      <div className="input-group">
        <input type="number" placeholder="Number A" value={a} onChange={e => setA(e.target.value)} />
      </div>
      <div className="input-group">
        <input type="number" placeholder="Number B" value={b} onChange={e => setB(e.target.value)} />
      </div>
      <div className="btn-group">
        <button onClick={() => calculate('add')}>Add (+)</button>
        <button onClick={() => calculate('subtract')}>Sub (-)</button>
        <button onClick={() => calculate('multiply')}>Mul (×)</button>
        <button onClick={() => calculate('divide')}>Div (÷)</button>
      </div>
      {result && (
        <div className="result-box">
          <strong>Result: {result.result !== undefined ? result.result : 'Error'}</strong>
          <div className="json-display">{JSON.stringify(result, null, 2)}</div>
        </div>
      )}
    </div>
  );
}

export default CalculatorCard;