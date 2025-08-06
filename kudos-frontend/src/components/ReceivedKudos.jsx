import React, { useState } from 'react';
import axios from 'axios';

function ReceivedKudos() {
  const [userId, setUserId] = useState('');
  const [kudos, setKudos] = useState([]);
  const [error, setError] = useState('');

  const fetchReceivedKudos = async () => {
    try {
      const response = await axios.get('http://localhost:8000/me/kudos/received', {
        headers: {
          'X-User-Id': userId
        }
      });
      setKudos(response.data);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Could not fetch kudos. Make sure the user ID is valid.');
    }
  };

  return (
    <div>
      <h2>Received Kudos</h2>
      <input
        type="number"
        placeholder="Enter your user ID"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
      />
      <button onClick={fetchReceivedKudos}>Fetch My Kudos</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {kudos.map((kudo) => (
          <li key={kudo.id}>
            <strong>From:</strong> User {kudo.giver_id} <br />
            <strong>Message:</strong> {kudo.message} <br />
            <strong>Time:</strong> {new Date(kudo.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReceivedKudos;
