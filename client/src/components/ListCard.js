import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function ListCard() {
  const [inputStr, setInputStr] = useState('5, 1, 9, 3');
  const [result, setResult] = useState(null);

  const sortNumbers = async (reverse) => {
    // Convert string "1, 2, 3" to array [1, 2, 3]
    const numbersArray = inputStr.split(',')
        .map(n => parseFloat(n.trim()))
        .filter(n => !isNaN(n));

    if (numbersArray.length === 0) {
      setResult({ error: "Please enter valid numbers separated by commas" });
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/api/list/sort`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numbers: numbersArray, reverse: reverse })
      });
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Fetch error" });
    }
  };

  return (
    <div className="card">
      <h2>📊 List Magic</h2>
      <p style={{fontSize: '0.8rem', color: '#a0a0a0', margin: '0 0 10px 0'}}>Enter numbers separated by commas</p>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="e.g. 5, 1, 8, 2" 
          value={inputStr} 
          onChange={e => setInputStr(e.target.value)} 
        />
      </div>
      <div className="btn-group">
        <button onClick={() => sortNumbers(false)}>Sort Asc (1-9)</button>
        <button onClick={() => sortNumbers(true)}>Sort Desc (9-1)</button>
      </div>
      
      {result && (
        <div className="result-box">
          {result.result && (
            <div style={{wordBreak: 'break-all'}}>
              <strong>Sorted: </strong>
              [{result.result.join(', ')}]
            </div>
          )}
           <div className="json-display" style={{marginTop: '10px'}}>
             {JSON.stringify(result)}
          </div>
        </div>
      )}
    </div>
  );
}

export default ListCard;