import React, { useState } from 'react';
import api from '../api';

export default function CreateUser() {
  const [form, setForm] = useState({
    username: '',
    email: '',
    password: '',
    org_name: ''
  });

  const handleChange = (e) => {
    setForm({...form, [e.target.name]: e.target.value});
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/users/', form);
      alert('User created: ' + res.data.username);
    } catch (err) {
      alert('Error: ' + err.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Create User</h2>
      <input name="username" placeholder="Username" onChange={handleChange} required />
      <input name="email" type="email" placeholder="Email" onChange={handleChange} required />
      <input name="password" type="password" placeholder="Password" onChange={handleChange} required />
      <input name="org_name" placeholder="Organization Name" onChange={handleChange} required />
      <button type="submit">Create User</button>
    </form>
  );
}
