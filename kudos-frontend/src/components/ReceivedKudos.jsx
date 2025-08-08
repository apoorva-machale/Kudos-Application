import React, { useState } from 'react';
import api from '../api';

function ReceivedKudos() {
  const [kudos, setKudos] = useState([]);
  const [error, setError] = useState('');
  const [remkudos, setremKudos] = useState(0);

  const fetchReceivedKudos = async () => {
    try {
      const res = await api.get('/me'); // /me returns received_kudos
      setremKudos(res.data.kudos_remaining);
      setKudos(res.data.received_kudos);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Could not fetch kudos. Make sure you are logged in.');
    }
  };

  return (
    <div>
      <button onClick={fetchReceivedKudos}>My Kudos Information</button>
      <h5>My remaining kudos</h5>
      <p>{remkudos}</p>
      <h5>Received Kudos</h5>
      
      {error && <p style={{ color: 'red' }}>{error}</p>}

      <ul>
        {kudos.map((kudo) => (
          <li key={kudo.id}>
            <strong>From:</strong> {kudo.giver_username} <br />
            <strong>Message:</strong> {kudo.message} <br />
            <strong>Time:</strong> {new Date(kudo.created_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ReceivedKudos;
