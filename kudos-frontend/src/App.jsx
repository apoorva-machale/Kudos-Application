import React from 'react';
import CreateOrganization from './components/CreateOrganization';
import CreateUser from './components/CreateUser';
import GiveKudos from './components/GiveKudos';
import ReceivedKudos from './components/ReceivedKudos';
import GenerateDemoData from './components/GenerateDemoData';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  return (
    <div className="app-container">
      {/* Top Navbar */}
      <header className="navbar">
        <h1 className="app-title">🎉 Kudos Application</h1>
        <nav className="nav-links">
          <a href="#dashboard">Dashboard</a>
          <a href="#givekudos">Give Kudos</a>
          <a href="#receivedkudos">Received Kudos</a>
          <a href="#login">Login</a>
        </nav>
      </header>

      {/* 3-column layout */}
      <div className="content">
        {/* Left Sidebar */}
        <aside className="sidebar">
          <h3>Quick Actions</h3>
          <GenerateDemoData />
          <CreateOrganization />
          <CreateUser />
        </aside>

        {/* Scrollable Middle Section */}
        <main className="main-section">
          <section id="dashboard">
            <Dashboard />
          </section>
          <section id="login">
            <Login />
          </section>

          <section id="givekudos">
            <GiveKudos />
          </section>

          

        </main>

        {/* Right Sidebar */}
        <aside className="right-sidebar">
          <section id="receivedkudos">
            <ReceivedKudos />
          </section>

        </aside>
      </div>
    </div>
  );
}

export default App;
