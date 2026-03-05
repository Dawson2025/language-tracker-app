// resource_id: 2145fb70-27fc-4c80-ae06-6d23e12355cd
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { vocabularyService, Word } from '../services/vocabularyService';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Alert } from '../components/ui/Alert';

interface PracticeSession {
  words: Word[];
  currentIndex: number;
  score: number;
  correctAnswers: number;
  totalAnswers: number;
  startTime: Date;
}

export const PracticePage: React.FC = () => {
  const [session, setSession] = useState<PracticeSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [userAnswer, setUserAnswer] = useState<string>('');
  const [showAnswer, setShowAnswer] = useState(false);
  const [feedback, setFeedback] = useState<{ type: 'correct' | 'incorrect' | ''; message: string }>({ type: '', message: '' });
  const [isCompleted, setIsCompleted] = useState(false);

  const { logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    startPracticeSession();
  }, []);

  const startPracticeSession = async () => {
    try {
      setIsLoading(true);
      setError('');

      // For now, use mock data since the backend practice API isn't implemented yet
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      
      // Mock practice words
      const mockWords: Word[] = [
        {
          id: 1,
          word: 'casa',
          translation: 'house',
          language: 'Spanish',
          target_language: 'English',
          category: 'Home',
          difficulty_level: 'beginner',
          pronunciation: 'KAH-sah',
          example_sentence: 'Mi casa es grande.',
          example_translation: 'My house is big.',
          notes: 'Common noun',
          created_at: '2025-01-15T10:00:00Z',
          updated_at: '2025-01-15T10:00:00Z',
          learning_progress: {
            id: 1,
            word_id: 1,
            user_id: 1,
            mastery_level: 60,
            last_reviewed: '2025-01-15T10:00:00Z',
            review_count: 3,
            correct_count: 2,
            incorrect_count: 1,
            next_review: '2025-01-16T10:00:00Z',
            is_mastered: false,
            created_at: '2025-01-15T10:00:00Z',
            updated_at: '2025-01-15T10:00:00Z',
          }
        },
        {
          id: 2,
          word: 'agua',
          translation: 'water',
          language: 'Spanish',
          target_language: 'English',
          category: 'Food & Drink',
          difficulty_level: 'beginner',
          pronunciation: 'AH-gwah',
          example_sentence: 'Necesito agua.',
          example_translation: 'I need water.',
          notes: 'Essential vocabulary',
          created_at: '2025-01-15T11:00:00Z',
          updated_at: '2025-01-15T11:00:00Z',
          learning_progress: {
            id: 2,
            word_id: 2,
            user_id: 1,
            mastery_level: 40,
            last_reviewed: '2025-01-15T09:00:00Z',
            review_count: 2,
            correct_count: 1,
            incorrect_count: 1,
            next_review: '2025-01-16T09:00:00Z',
            is_mastered: false,
            created_at: '2025-01-15T11:00:00Z',
            updated_at: '2025-01-15T11:00:00Z',
          }
        },
        {
          id: 3,
          word: 'tiempo',
          translation: 'time/weather',
          language: 'Spanish',
          target_language: 'English',
          category: 'Abstract',
          difficulty_level: 'intermediate',
          pronunciation: 'tee-EHM-poh',
          example_sentence: 'No tengo tiempo.',
          example_translation: 'I don\'t have time.',
          notes: 'Multiple meanings',
          created_at: '2025-01-15T12:00:00Z',
          updated_at: '2025-01-15T12:00:00Z',
          learning_progress: {
            id: 3,
            word_id: 3,
            user_id: 1,
            mastery_level: 20,
            last_reviewed: null,
            review_count: 0,
            correct_count: 0,
            incorrect_count: 0,
            next_review: null,
            is_mastered: false,
            created_at: '2025-01-15T12:00:00Z',
            updated_at: '2025-01-15T12:00:00Z',
          }
        }
      ];

      setSession({
        words: mockWords,
        currentIndex: 0,
        score: 0,
        correctAnswers: 0,
        totalAnswers: 0,
        startTime: new Date()
      });

    } catch (err) {
      console.error('Error starting practice session:', err);
      setError('Practice sessions will be implemented in the next phase. This is preview data.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitAnswer = () => {
    if (!session || !userAnswer.trim()) return;

    const currentWord = session.words[session.currentIndex];
    const isCorrect = userAnswer.toLowerCase().trim() === currentWord.translation.toLowerCase().trim();
    
    setFeedback({
      type: isCorrect ? 'correct' : 'incorrect',
      message: isCorrect 
        ? '🎉 Correct! Well done!' 
        : `❌ Incorrect. The correct answer is: ${currentWord.translation}`
    });

    setSession(prev => prev ? {
      ...prev,
      score: isCorrect ? prev.score + 1 : prev.score,
      correctAnswers: isCorrect ? prev.correctAnswers + 1 : prev.correctAnswers,
      totalAnswers: prev.totalAnswers + 1
    } : null);

    setShowAnswer(true);
  };

  const handleNextWord = () => {
    if (!session) return;

    setUserAnswer('');
    setShowAnswer(false);
    setFeedback({ type: '', message: '' });

    if (session.currentIndex + 1 >= session.words.length) {
      // Session completed
      setIsCompleted(true);
    } else {
      setSession(prev => prev ? {
        ...prev,
        currentIndex: prev.currentIndex + 1
      } : null);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      if (showAnswer) {
        handleNextWord();
      } else {
        handleSubmitAnswer();
      }
    }
  };

  const getProgressPercentage = () => {
    if (!session) return 0;
    return Math.round(((session.currentIndex + (showAnswer ? 1 : 0)) / session.words.length) * 100);
  };

  const getSessionDuration = () => {
    if (!session) return 0;
    return Math.round((new Date().getTime() - session.startTime.getTime()) / 1000);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (isCompleted && session) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-lg text-center">
          <span className="text-6xl mb-4 block">🎉</span>
          <h1 className="text-2xl font-bold text-gray-900 mb-4">Practice Complete!</h1>
          
          <div className="space-y-4 mb-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <div className="text-3xl font-bold text-primary-600">
                {Math.round((session.correctAnswers / session.totalAnswers) * 100)}%
              </div>
              <div className="text-sm text-gray-600">Accuracy</div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div className="p-3 bg-green-50 rounded-lg">
                <div className="font-semibold text-green-700">{session.correctAnswers}</div>
                <div className="text-green-600">Correct</div>
              </div>
              <div className="p-3 bg-red-50 rounded-lg">
                <div className="font-semibold text-red-700">{session.totalAnswers - session.correctAnswers}</div>
                <div className="text-red-600">Incorrect</div>
              </div>
            </div>
            
            <div className="text-sm text-gray-600">
              Session duration: {Math.floor(getSessionDuration() / 60)}:{(getSessionDuration() % 60).toString().padStart(2, '0')}
            </div>
          </div>

          <div className="space-y-3">
            <button
              onClick={startPracticeSession}
              className="btn-primary w-full"
              disabled
            >
              Practice Again
            </button>
            <Link
              to="/vocabulary"
              className="btn-secondary w-full block text-center"
            >
              Back to Vocabulary
            </Link>
            <Link
              to="/dashboard"
              className="text-primary-600 hover:text-primary-700 text-sm"
            >
              Return to Dashboard
            </Link>
          </div>
        </div>
      </div>
    );
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <span className="text-4xl mb-4 block">❌</span>
          <h1 className="text-xl font-semibold text-gray-900 mb-4">Unable to load practice session</h1>
          <Link to="/dashboard" className="btn-primary">
            Return to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  const currentWord = session.words[session.currentIndex];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-sm border border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Link to="/dashboard" className="text-2xl font-bold text-gray-900">
                🗣️ Language Tracker
              </Link>
              <span className="text-gray-600">→</span>
              <span className="text-lg font-medium text-gray-900">Practice</span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                to="/dashboard"
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Dashboard
              </Link>
              <button
                onClick={logout}
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6">
            <Alert variant="warning" message={error} />
          </div>
        )}

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">
              Question {session.currentIndex + 1} of {session.words.length}
            </span>
            <span className="text-sm font-medium text-gray-700">
              Score: {session.correctAnswers}/{session.totalAnswers}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${getProgressPercentage()}%` }}
            ></div>
          </div>
        </div>

        {/* Practice Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 text-center">
          <div className="mb-6">
            <div className="text-sm text-gray-500 mb-2">
              {currentWord.language} → {currentWord.target_language}
            </div>
            <div className="text-4xl font-bold text-gray-900 mb-4">
              {currentWord.word}
            </div>
            {currentWord.pronunciation && (
              <div className="text-lg text-gray-600 mb-2">
                /{currentWord.pronunciation}/
              </div>
            )}
            {currentWord.category && (
              <span className="px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-600">
                {currentWord.category}
              </span>
            )}
          </div>

          {currentWord.example_sentence && !showAnswer && (
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <p className="text-gray-700 italic">"{currentWord.example_sentence}"</p>
            </div>
          )}

          <div className="mb-6">
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your answer..."
              className="input-field text-center text-lg"
              disabled={showAnswer}
              autoFocus
            />
          </div>

          {feedback.message && (
            <div className="mb-6">
              <Alert 
                variant={feedback.type === 'correct' ? 'success' : 'error'} 
                message={feedback.message} 
              />
            </div>
          )}

          {showAnswer && currentWord.example_translation && (
            <div className="mb-6 p-4 bg-blue-50 rounded-lg">
              <p className="text-blue-700">"{currentWord.example_translation}"</p>
            </div>
          )}

          <div className="space-y-3">
            {!showAnswer ? (
              <button
                onClick={handleSubmitAnswer}
                disabled={!userAnswer.trim()}
                className="btn-primary w-full disabled:opacity-50"
              >
                Submit Answer
              </button>
            ) : (
              <button
                onClick={handleNextWord}
                className="btn-primary w-full"
              >
                {session.currentIndex + 1 >= session.words.length ? 'Finish Session' : 'Next Word'}
              </button>
            )}

            <Link
              to="/vocabulary"
              className="btn-secondary w-full block text-center"
            >
              Exit Practice
            </Link>
          </div>

          <div className="mt-6 text-xs text-gray-500">
            Press Enter to {showAnswer ? 'continue' : 'submit'}
          </div>
        </div>
      </main>
    </div>
  );
};