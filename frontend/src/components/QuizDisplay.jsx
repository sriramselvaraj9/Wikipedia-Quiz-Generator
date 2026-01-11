import React, { useState } from 'react';

function QuizDisplay({ quizData }) {
  const [quizMode, setQuizMode] = useState('view'); // 'view' or 'take'
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  const handleAnswerSelect = (questionIndex, selectedOption) => {
    if (showResults) return;
    setAnswers({
      ...answers,
      [questionIndex]: selectedOption,
    });
  };

  const handleSubmitQuiz = () => {
    setShowResults(true);
  };

  const calculateScore = () => {
    let correct = 0;
    quizData.quiz.forEach((question, index) => {
      if (answers[index] === question.answer) {
        correct++;
      }
    });
    return correct;
  };

  const resetQuiz = () => {
    setAnswers({});
    setShowResults(false);
  };

  return (
    <div>
      {/* Quiz Header */}
      <div className="card">
        <div className="quiz-header">
          <h2>{quizData.title}</h2>
          <a
            href={quizData.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{ color: 'var(--primary-color)', fontSize: '0.875rem' }}
          >
            View Original Article →
          </a>
        </div>
        
        <div className="quiz-summary">
          <p>{quizData.summary}</p>
        </div>

        {/* Key Entities */}
        {quizData.key_entities && (
          <div className="entities">
            {quizData.key_entities.people && quizData.key_entities.people.length > 0 && (
              <div className="entity-group">
                <h4>👤 People</h4>
                <div className="entity-tags">
                  {quizData.key_entities.people.map((person, idx) => (
                    <span key={idx} className="tag">{person}</span>
                  ))}
                </div>
              </div>
            )}
            {quizData.key_entities.organizations && quizData.key_entities.organizations.length > 0 && (
              <div className="entity-group">
                <h4>🏢 Organizations</h4>
                <div className="entity-tags">
                  {quizData.key_entities.organizations.map((org, idx) => (
                    <span key={idx} className="tag">{org}</span>
                  ))}
                </div>
              </div>
            )}
            {quizData.key_entities.locations && quizData.key_entities.locations.length > 0 && (
              <div className="entity-group">
                <h4>📍 Locations</h4>
                <div className="entity-tags">
                  {quizData.key_entities.locations.map((loc, idx) => (
                    <span key={idx} className="tag">{loc}</span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Quiz Mode Toggle */}
        <div style={{ marginTop: '1.5rem', display: 'flex', gap: '0.5rem' }}>
          <button
            onClick={() => {
              setQuizMode('view');
              resetQuiz();
            }}
            className={`btn ${quizMode === 'view' ? 'btn-primary' : 'btn-secondary'}`}
          >
            📖 View Mode
          </button>
          <button
            onClick={() => {
              setQuizMode('take');
              resetQuiz();
            }}
            className={`btn ${quizMode === 'take' ? 'btn-primary' : 'btn-secondary'}`}
          >
            ✍️ Take Quiz Mode
          </button>
        </div>
      </div>

      {/* Quiz Score (only in take mode after submission) */}
      {quizMode === 'take' && showResults && (
        <div className="quiz-score">
          <h2>{calculateScore()} / {quizData.quiz.length}</h2>
          <p>
            {calculateScore() === quizData.quiz.length
              ? '🎉 Perfect Score!'
              : calculateScore() >= quizData.quiz.length * 0.7
              ? '👏 Great job!'
              : '💪 Keep learning!'}
          </p>
          <button
            onClick={resetQuiz}
            className="btn btn-secondary"
            style={{ marginTop: '1rem' }}
          >
            🔄 Retake Quiz
          </button>
        </div>
      )}

      {/* Questions */}
      <div>
        <h3 style={{ marginBottom: '1rem' }}>
          {quizMode === 'view' ? '📝 Quiz Questions & Answers' : '✍️ Answer the Questions'}
        </h3>
        {quizData.quiz.map((question, index) => (
          <div key={index} className="card question-card">
            <div className="question-header">
              <div className="question-text">
                <span style={{ fontWeight: '700', marginRight: '0.5rem' }}>Q{index + 1}.</span>
                {question.question}
              </div>
              <span className={`difficulty-badge difficulty-${question.difficulty}`}>
                {question.difficulty}
              </span>
            </div>

            <div className="options">
              {question.options.map((option, optionIndex) => {
                const isSelected = answers[index] === option;
                const isCorrect = option === question.answer;
                const showCorrect = quizMode === 'view' || showResults;

                let optionClass = 'option';
                if (quizMode === 'take') {
                  if (isSelected && !showResults) optionClass += ' selected';
                  if (showResults) {
                    if (isCorrect) optionClass += ' correct';
                    else if (isSelected && !isCorrect) optionClass += ' incorrect';
                  }
                } else {
                  if (isCorrect) optionClass += ' correct';
                }

                return (
                  <div
                    key={optionIndex}
                    className={optionClass}
                    onClick={() => quizMode === 'take' && handleAnswerSelect(index, option)}
                  >
                    <span style={{ fontWeight: '500', marginRight: '0.5rem' }}>
                      {String.fromCharCode(65 + optionIndex)}.
                    </span>
                    {option}
                    {showCorrect && isCorrect && <span style={{ marginLeft: '0.5rem' }}>✓</span>}
                  </div>
                );
              })}
            </div>

            {(quizMode === 'view' || showResults) && (
              <div className="explanation">
                <strong>💡 Explanation:</strong> {question.explanation}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Submit Button (take mode only) */}
      {quizMode === 'take' && !showResults && (
        <div style={{ textAlign: 'center', marginTop: '2rem' }}>
          <button
            onClick={handleSubmitQuiz}
            className="btn btn-primary"
            disabled={Object.keys(answers).length !== quizData.quiz.length}
            style={{ fontSize: '1.125rem', padding: '1rem 2rem' }}
          >
            {Object.keys(answers).length === quizData.quiz.length
              ? '✅ Submit Quiz'
              : `Answer all questions (${Object.keys(answers).length}/${quizData.quiz.length})`}
          </button>
        </div>
      )}

      {/* Related Topics */}
      {quizData.related_topics && quizData.related_topics.length > 0 && (
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>🔗 Related Topics for Further Reading</h3>
          <div className="related-topics">
            {quizData.related_topics.map((topic, index) => (
              <a
                key={index}
                href={`https://en.wikipedia.org/wiki/${topic.replace(/ /g, '_')}`}
                target="_blank"
                rel="noopener noreferrer"
                className="topic-tag"
              >
                {topic}
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Sections */}
      {quizData.sections && quizData.sections.length > 0 && (
        <div className="card">
          <h3 style={{ marginBottom: '1rem' }}>📑 Article Sections</h3>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
            {quizData.sections.map((section, index) => (
              <span key={index} className="tag">{section}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default QuizDisplay;
