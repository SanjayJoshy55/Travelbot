import React from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  return (
    <div className="app-container">
      <header>
        <h1>Exploreain AI 🌍</h1>
        <p style={{ opacity: 0.8 }}>Your Intelligent RAG-Powered Travel Companion</p>
      </header>
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <ChatInterface />
      </main>
    </div>
  );
}

export default App;
