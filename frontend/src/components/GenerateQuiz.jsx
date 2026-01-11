import React, { useState } from 'react';
import { generateQuiz } from '../services/api';
import QuizDisplay from './QuizDisplay';

function GenerateQuiz() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [quizData, setQuizData] = useState(null);
  const [forceRegenerate, setForceRegenerate] = useState(false);

  const validateUrl = (url) => {
    const pattern = /^https?:\/\/[a-z]{2,3}\.wikipedia\.org\/wiki\/.+$/;
    return pattern.test(url);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setQuizData(null);

    if (!url.trim()) {
      setError('Please enter a Wikipedia URL');
      return;
    }

    if (!validateUrl(url)) {
      setError('Please enter a valid Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)');
      return;
    }

    setLoading(true);

    try {
      const data = await generateQuiz(url, forceRegenerate, false);
      setQuizData(data);
      setError('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate quiz. Please try again.');
      console.error('Error generating quiz:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleNewQuiz = () => {
    setQuizData(null);
    setUrl('');
    setError('');
  };

  return (
    <div>
      {!quizData ? (
        <div className="card">
          <h2 style={{ marginBottom: '1rem' }}>Generate a New Quiz</h2>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
            Enter a Wikipedia article URL to generate an AI-powered quiz
          </p>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="input-group">
              <label htmlFor="url">Wikipedia Article URL</label>
              <input
                type="text"
                id="url"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="https://en.wikipedia.org/wiki/Alan_Turing"
                disabled={loading}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
                <input
                  type="checkbox"
                  checked={forceRegenerate}
                  onChange={(e) => setForceRegenerate(e.target.checked)}
                  disabled={loading}
                />
                <span style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                  Force regenerate (ignore cache)
                </span>
              </label>
            </div>

            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <div className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></div>
                  Generating Quiz...
                </>
              ) : (
                <>
                  ✨ Generate Quiz
                </>
              )}
            </button>
          </form>

          <div style={{ marginTop: '2rem', padding: '1rem', background: 'var(--background)', borderRadius: '8px' }}>
            <h3 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>💡 Try these examples:</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
              {[
                'https://en.wikipedia.org/wiki/Alan_Turing',
                'https://en.wikipedia.org/wiki/Artificial_intelligence',
                'https://en.wikipedia.org/wiki/World_War_II',
                'https://en.wikipedia.org/wiki/Albert_Einstein',
              ].map((exampleUrl) => (
                <button
                  key={exampleUrl}
                  onClick={() => setUrl(exampleUrl)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-color)',
                    cursor: 'pointer',
                    textAlign: 'left',
                    padding: '0.25rem',
                    fontSize: '0.875rem',
                  }}
                >
                  {exampleUrl}
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : (
        <div>
          <div style={{ marginBottom: '1rem' }}>
            <button onClick={handleNewQuiz} className="btn btn-secondary">
              ← Generate Another Quiz
            </button>
          </div>
          <QuizDisplay quizData={quizData} />
        </div>
      )}
    </div>
  );
}

export default GenerateQuiz;
