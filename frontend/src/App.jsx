import React, { useState } from 'react';
import GenerateQuiz from './components/GenerateQuiz';
import QuizHistory from './components/QuizHistory';

function App() {
  const [activeTab, setActiveTab] = useState('generate');

  return (
    <div className="app">
      <header className="header">
        <div className="container">
          <h1>📚 Wikipedia Quiz Generator</h1>
          <p>Transform any Wikipedia article into an interactive quiz using AI</p>
        </div>
      </header>

      <div className="container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            🎯 Generate Quiz
          </button>
          <button
            className={`tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            📖 Past Quizzes
          </button>
        </div>

        {activeTab === 'generate' ? <GenerateQuiz /> : <QuizHistory />}
      </div>
    </div>
  );
}

export default App;
