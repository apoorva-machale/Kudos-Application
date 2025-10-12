import React, { useState } from 'react';
import api from '../api';

export default function CreateOrganization() {
  const [name, setName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/organizations/', { name });
      alert('Organization created: ' + res.data.name);
    } catch (err) {
  alert('Error: ' + (err.response?.data?.detail || err.message));
}
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create Organization</h2>
      <input
        type="text"
        placeholder="Organization Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <button type="submit">Create</button>
    </form>
  );
}
