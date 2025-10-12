import React, { useState } from 'react';
import api from '../api';

export default function GiveKudos() {
  const [receiverUsername, setReceiverUsername] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post('/kudos/', {
        receiver_username: receiverUsername,
        message
      });
      alert('Kudos sent!');
    } catch (err) {
      alert('Error: ' + err.response?.data?.detail || err.message);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Give Kudos</h2>
      <input
        type="text"
        placeholder="Receiver Username"
        value={receiverUsername}
        onChange={(e) => setReceiverUsername(e.target.value)}
        required
      />
      <input
        type="text"
        placeholder="Message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button type="submit">Send Kudos</button>
    </form>
  );
}
