import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function StringCard() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);

  const handleAction = async (endpoint) => {
    if (!text) return;
    try {
      const res = await fetch(`${API_BASE_URL}/string/${endpoint}?text=${encodeURIComponent(text)}`);
      const data = await res.json();
      setResult(data);
    } catch (error) {
      setResult({ error: "Fetch error" });
    }
  };

  return (
    <div className="card">
      <h2>🔤 String Tools</h2>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter text..." 
          value={text} 
          onChange={e => setText(e.target.value)} 
        />
      </div>
      <div className="btn-group">
        <button onClick={() => handleAction('palindrome')}>Check Palindrome</button>
        <button onClick={() => handleAction('reverse')}>Reverse Text</button>
      </div>
      
      {result && (
        <div className="result-box">
          {result.is_palindrome !== undefined && (
            <strong>Is Palindrome: {result.is_palindrome ? "✅ Yes" : "❌ No"}</strong>
          )}
          {result.result && (
            <strong>Reversed: {result.result}</strong>
          )}
          <div className="json-display" style={{marginTop: '10px'}}>
             {JSON.stringify(result, null, 2)}
          </div>
        </div>
      )}
    </div>
  );
}

export default StringCard;