import React, { useEffect, useState } from 'react';
import api from '../api';

export default function Dashboard() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await api.get('/me');
        setUser(res.data);
      } catch (err) {
        console.error(err);
        setError('Could not fetch user details. Please log in again.');
      }
    };
    fetchUser();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/login';
  };

  return (
    <div style={{ padding: '20px' }}>
      <h2>Dashboard</h2>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {user ? (
        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          {/* Box 1 - User Info */}
          <div style={{ padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Logged in as</h3>
            <p><strong>Username:</strong> {user.username}</p>
          </div>

          {/* Box 2 - Organization Info */}
          <div style={{ padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
            <h3>Organization</h3>
            <p>{user.organization}</p>
          </div>
        </div>
      ) : (
        <p>Loading user details...</p>
      )}

      <button onClick={handleLogout} style={{ background: 'red', color: 'white', padding: '10px 15px', border: 'none', borderRadius: '5px' }}>
        Logout
      </button>
    </div>
  );
}
