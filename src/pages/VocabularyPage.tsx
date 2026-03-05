// resource_id: ae8763af-b8f3-431a-b675-110222df4df7
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { vocabularyService, Word, Category, WordFilters, PaginatedResponse } from '../services/vocabularyService';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Alert } from '../components/ui/Alert';

export const VocabularyPage: React.FC = () => {
  const [words, setWords] = useState<PaginatedResponse<Word> | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string>('');
  const [showAddWord, setShowAddWord] = useState(false);
  const [selectedWord, setSelectedWord] = useState<Word | null>(null);
  const [filters, setFilters] = useState<WordFilters>({});
  const [currentPage, setCurrentPage] = useState(1);

  const { user, logout } = useAuth();

  useEffect(() => {
    loadVocabularyData();
  }, [currentPage, filters]);

  const loadVocabularyData = async () => {
    try {
      setIsLoading(true);
      setError('');

      // For now, use mock data since the backend vocabulary API isn't implemented yet
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      
      // Mock vocabulary data
      const mockWords: Word[] = [
        {
          id: 1,
          word: 'hola',
          translation: 'hello',
          language: 'Spanish',
          target_language: 'English',
          category: 'Greetings',
          difficulty_level: 'beginner',
          pronunciation: 'OH-lah',
          example_sentence: 'Hola, ¿cómo estás?',
          example_translation: 'Hello, how are you?',
          notes: 'Common greeting',
          created_at: '2025-01-15T10:00:00Z',
          updated_at: '2025-01-15T10:00:00Z',
          learning_progress: {
            id: 1,
            word_id: 1,
            user_id: 1,
            mastery_level: 75,
            last_reviewed: '2025-01-15T10:00:00Z',
            review_count: 5,
            correct_count: 4,
            incorrect_count: 1,
            next_review: '2025-01-16T10:00:00Z',
            is_mastered: false,
            created_at: '2025-01-15T10:00:00Z',
            updated_at: '2025-01-15T10:00:00Z',
          }
        },
        {
          id: 2,
          word: 'gracias',
          translation: 'thank you',
          language: 'Spanish',
          target_language: 'English',
          category: 'Politeness',
          difficulty_level: 'beginner',
          pronunciation: 'GRAH-see-ahs',
          example_sentence: 'Gracias por tu ayuda.',
          example_translation: 'Thank you for your help.',
          notes: 'Expression of gratitude',
          created_at: '2025-01-15T11:00:00Z',
          updated_at: '2025-01-15T11:00:00Z',
          learning_progress: {
            id: 2,
            word_id: 2,
            user_id: 1,
            mastery_level: 90,
            last_reviewed: '2025-01-15T11:00:00Z',
            review_count: 8,
            correct_count: 7,
            incorrect_count: 1,
            next_review: '2025-01-17T11:00:00Z',
            is_mastered: true,
            created_at: '2025-01-15T11:00:00Z',
            updated_at: '2025-01-15T11:00:00Z',
          }
        }
      ];

      const mockCategories: Category[] = [
        { id: 1, name: 'Greetings', description: 'Common greetings and salutations', color: '#3b82f6', created_at: '2025-01-15T10:00:00Z', word_count: 5 },
        { id: 2, name: 'Politeness', description: 'Polite expressions and courtesy words', color: '#10b981', created_at: '2025-01-15T10:00:00Z', word_count: 3 },
        { id: 3, name: 'Family', description: 'Family members and relationships', color: '#f59e0b', created_at: '2025-01-15T10:00:00Z', word_count: 8 }
      ];

      setWords({
        items: mockWords,
        page: currentPage,
        pages: 1,
        per_page: 20,
        total: mockWords.length,
        has_next: false,
        has_prev: false
      });
      
      setCategories(mockCategories);

    } catch (err) {
      console.error('Error loading vocabulary:', err);
      setError('Vocabulary features will be implemented in the next phase. This is preview data.');
    } finally {
      setIsLoading(false);
    }
  };

  const getMasteryColor = (level: number) => {
    if (level >= 90) return 'text-green-600';
    if (level >= 70) return 'text-yellow-600';
    if (level >= 50) return 'text-orange-600';
    return 'text-red-600';
  };

  const getMasteryLabel = (level: number, isMastered: boolean) => {
    if (isMastered) return 'Mastered';
    if (level >= 70) return 'Learning';
    if (level >= 30) return 'Practicing';
    return 'New';
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

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
              <span className="text-lg font-medium text-gray-900">Vocabulary</span>
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

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">My Vocabulary</h1>
            <p className="text-gray-600">
              Manage your words and track your learning progress
            </p>
          </div>
          <button
            onClick={() => setShowAddWord(true)}
            className="btn-primary"
            disabled
          >
            Add New Word
          </button>
        </div>

        {error && (
          <div className="mb-6">
            <Alert variant="warning" message={error} />
          </div>
        )}

        {/* Categories Section */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Categories</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {categories.map(category => (
              <div
                key={category.id}
                className="bg-white p-4 rounded-lg shadow-sm border border-gray-200"
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900">{category.name}</h3>
                  <span
                    className="w-3 h-3 rounded-full"
                    style={{ backgroundColor: category.color }}
                  ></span>
                </div>
                <p className="text-sm text-gray-600 mb-3">{category.description}</p>
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>{category.word_count} words</span>
                  <button
                    onClick={() => setFilters({ ...filters, category: category.name })}
                    className="text-primary-600 hover:text-primary-700"
                  >
                    View Words
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Words Section */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <div className="flex justify-between items-center">
              <h2 className="text-lg font-semibold text-gray-900">Words</h2>
              <div className="flex items-center space-x-4">
                <select
                  className="input-field"
                  value={filters.category || ''}
                  onChange={(e) => setFilters({ ...filters, category: e.target.value || undefined })}
                >
                  <option value="">All Categories</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.name}>{cat.name}</option>
                  ))}
                </select>
                <select
                  className="input-field"
                  value={filters.difficulty_level || ''}
                  onChange={(e) => setFilters({ ...filters, difficulty_level: e.target.value || undefined })}
                >
                  <option value="">All Levels</option>
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                </select>
              </div>
            </div>
          </div>

          <div className="divide-y divide-gray-200">
            {words && words.items.length > 0 ? (
              words.items.map((word) => (
                <div key={word.id} className="px-6 py-4 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-4">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            {word.word}
                          </h3>
                          <p className="text-gray-600">{word.translation}</p>
                        </div>
                        {word.pronunciation && (
                          <div className="text-sm text-gray-500">
                            /{word.pronunciation}/
                          </div>
                        )}
                      </div>
                      
                      <div className="flex items-center space-x-6 mt-2 text-sm text-gray-500">
                        <span className="flex items-center">
                          <span className="font-medium">{word.language}</span>
                          <span className="mx-1">→</span>
                          <span className="font-medium">{word.target_language}</span>
                        </span>
                        {word.category && (
                          <span className="px-2 py-1 bg-gray-100 rounded-full text-xs">
                            {word.category}
                          </span>
                        )}
                        <span className="capitalize">{word.difficulty_level}</span>
                      </div>

                      {word.example_sentence && (
                        <div className="mt-3 p-3 bg-gray-50 rounded-md">
                          <p className="text-sm text-gray-700 italic">"{word.example_sentence}"</p>
                          {word.example_translation && (
                            <p className="text-sm text-gray-600 mt-1">"{word.example_translation}"</p>
                          )}
                        </div>
                      )}
                    </div>

                    <div className="flex flex-col items-end space-y-2">
                      <div className="text-right">
                        <div className={`text-sm font-medium ${getMasteryColor(word.learning_progress.mastery_level)}`}>
                          {getMasteryLabel(word.learning_progress.mastery_level, word.learning_progress.is_mastered)}
                        </div>
                        <div className="text-xs text-gray-500">
                          {word.learning_progress.mastery_level}% mastery
                        </div>
                      </div>
                      
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => setSelectedWord(word)}
                          className="text-sm text-primary-600 hover:text-primary-700"
                          disabled
                        >
                          Practice
                        </button>
                        <button
                          onClick={() => console.log('Edit word', word.id)}
                          className="text-sm text-gray-600 hover:text-gray-700"
                          disabled
                        >
                          Edit
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="px-6 py-12 text-center">
                <span className="text-4xl mb-4 block">📚</span>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No words yet</h3>
                <p className="text-gray-600 mb-4">
                  Start building your vocabulary by adding your first word.
                </p>
                <button
                  onClick={() => setShowAddWord(true)}
                  className="btn-primary"
                  disabled
                >
                  Add Your First Word
                </button>
              </div>
            )}
          </div>

          {/* Pagination */}
          {words && words.pages > 1 && (
            <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
              <div className="text-sm text-gray-600">
                Showing {words.items.length} of {words.total} words
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={() => setCurrentPage(currentPage - 1)}
                  disabled={!words.has_prev}
                  className="btn-secondary text-sm px-3 py-1 disabled:opacity-50"
                >
                  Previous
                </button>
                <span className="px-3 py-1 text-sm text-gray-600">
                  Page {words.page} of {words.pages}
                </span>
                <button
                  onClick={() => setCurrentPage(currentPage + 1)}
                  disabled={!words.has_next}
                  className="btn-secondary text-sm px-3 py-1 disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};