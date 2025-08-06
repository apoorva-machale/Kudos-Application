import React, { useState } from 'react';
import api from '../api';

export default function GiveKudos() {
  const [receiverId, setReceiverId] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/kudos/', {
        receiver_id: parseInt(receiverId),
        message,
      });
      alert('Kudos sent!');
    } catch (err) {
      alert('Error: ' + err.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Give Kudos</h2>
      <input
        type="number"
        placeholder="Receiver ID"
        value={receiverId}
        onChange={(e) => setReceiverId(e.target.value)}
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
