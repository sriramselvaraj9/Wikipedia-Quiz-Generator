import React, { useState, useEffect } from 'react';
import { getQuizHistory, getQuizById, deleteQuiz } from '../services/api';
import QuizDisplay from './QuizDisplay';

function QuizHistory() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      const data = await getQuizHistory();
      setHistory(data);
      setError('');
    } catch (err) {
      setError('Failed to load quiz history');
      console.error('Error fetching history:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = async (quizId) => {
    try {
      const quiz = await getQuizById(quizId);
      setSelectedQuiz(quiz);
      setShowModal(true);
    } catch (err) {
      setError('Failed to load quiz details');
      console.error('Error fetching quiz:', err);
    }
  };

  const handleDelete = async (quizId) => {
    if (!confirm('Are you sure you want to delete this quiz?')) {
      return;
    }

    try {
      await deleteQuiz(quizId);
      setHistory(history.filter((quiz) => quiz.id !== quizId));
    } catch (err) {
      setError('Failed to delete quiz');
      console.error('Error deleting quiz:', err);
    }
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedQuiz(null);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading quiz history...</p>
      </div>
    );
  }

  if (error) {
    return <div className="error">{error}</div>;
  }

  if (history.length === 0) {
    return (
      <div className="card empty-state">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
          />
        </svg>
        <h3>No Quizzes Yet</h3>
        <p>Generate your first quiz from the "Generate Quiz" tab</p>
      </div>
    );
  }

  return (
    <div>
      <div className="card">
        <h2 style={{ marginBottom: '1rem' }}>📖 Past Quizzes</h2>
        <p style={{ color: 'var(--text-secondary)', marginBottom: '1.5rem' }}>
          View and manage all previously generated quizzes
        </p>

        <div style={{ overflowX: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>URL</th>
                <th>Questions</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {history.map((quiz) => (
                <tr key={quiz.id}>
                  <td style={{ fontWeight: '500' }}>{quiz.title}</td>
                  <td>
                    <a
                      href={quiz.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: 'var(--primary-color)',
                        textDecoration: 'none',
                        fontSize: '0.875rem',
                      }}
                    >
                      View Article →
                    </a>
                  </td>
                  <td>{quiz.quiz_count} questions</td>
                  <td style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                    {formatDate(quiz.created_at)}
                  </td>
                  <td>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        onClick={() => handleViewDetails(quiz.id)}
                        className="btn btn-primary"
                        style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                      >
                        📄 Details
                      </button>
                      <button
                        onClick={() => handleDelete(quiz.id)}
                        className="btn btn-danger"
                        style={{ padding: '0.5rem 1rem', fontSize: '0.875rem' }}
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Modal for Quiz Details */}
      {showModal && selectedQuiz && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Quiz Details</h2>
              <button onClick={closeModal} className="modal-close">
                ×
              </button>
            </div>
            <div className="modal-body">
              <QuizDisplay quizData={selectedQuiz} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizHistory;
