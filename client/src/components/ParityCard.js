import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function ParityCard() {
  const [n, setN] = useState('');
  const [data, setData] = useState(null);

  const checkParity = async () => {
    if (!n) return;
    try {
      const res = await fetch(`${API_BASE_URL}/parity/${n}`);
      const json = await res.json();
      setData(json);
    } catch (error) {
      setData({ error: "Fetch error" });
    }
  };

  return (
    <div className="card">
      <h2>⚖️ Parity Check</h2>
      <div className="input-group">
        <input 
          type="number" 
          placeholder="Enter Integer" 
          value={n} 
          onChange={e => setN(e.target.value)} 
        />
      </div>
      <button onClick={checkParity} style={{width: '100%'}}>Check Odd/Even</button>
      
      {data && !data.error && (
        <div className="result-box" style={{ borderColor: data.is_even ? '#4caf50' : '#ff9800' }}>
          <h3 style={{margin: 0}}>It is {data.parity.toUpperCase()}</h3>
          <p style={{fontSize: '0.9rem', color: '#a0a0a0'}}>
            Is Even: {data.is_even.toString()} <br/>
            Is Odd: {data.is_odd.toString()}
          </p>
        </div>
      )}
    </div>
  );
}

export default ParityCard;