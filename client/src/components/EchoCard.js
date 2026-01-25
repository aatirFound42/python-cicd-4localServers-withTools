import React, { useState } from 'react';
import { API_BASE_URL } from '../config';

function EchoCard() {
  const [msg, setMsg] = useState('');
  const [response, setResponse] = useState(null);

  const sendEcho = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/echo`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg })
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="card">
      <h2>📢 Echo Service</h2>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Type a message..." 
          value={msg} 
          onChange={e => setMsg(e.target.value)} 
        />
      </div>
      <button onClick={sendEcho} style={{width: '100%'}}>Send to API</button>
      
      {response && (
        <div className="result-box">
          <div><strong>Server returned:</strong> "{response.message}"</div>
          <div className="json-display" style={{marginTop: '10px'}}>
            {JSON.stringify(response)}
          </div>
        </div>
      )}
    </div>
  );
}

export default EchoCard;