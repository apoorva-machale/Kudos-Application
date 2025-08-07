import React from 'react';
import api from '../api';

export default function GenerateDemoData() {
  const handleClick = async () => {
    try {
      await api.post('/generate-demo-data');
      alert('Demo data created');
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  return (
    <div>
      <button onClick={handleClick}>Generate Demo Data</button>
    </div>
  );
}
