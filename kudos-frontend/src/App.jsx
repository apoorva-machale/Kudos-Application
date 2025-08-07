import React from 'react';
import CreateOrganization from './components/CreateOrganization';
import CreateUser from './components/CreateUser';
import GiveKudos from './components/GiveKudos';
import ReceivedKudos from './components/ReceivedKudos';
import GenerateDemoData from './components/GenerateDemoData';

function App() {
  return (
    <div>
      <h1>Kudos App</h1>
      <CreateOrganization />
      <CreateUser />
      <GiveKudos />
      <ReceivedKudos />
      <GenerateDemoData />
    </div>
  );
}

export default App;
