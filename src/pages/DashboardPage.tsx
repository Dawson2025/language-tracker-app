import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { LoadingSpinner } from '../components/ui/LoadingSpinner';
import { Alert } from '../components/ui/Alert';

interface DashboardStats {
  totalWords: number;
  wordsLearned: number;
  studyStreak: number;
  sessionsCompleted: number;
}

interface RecentActivity {
  id: string;
  type: 'vocabulary' | 'practice' | 'achievement';
  title: string;
  description: string;
  timestamp: Date;
}

export const DashboardPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats>({
    totalWords: 0,
    wordsLearned: 0,
    studyStreak: 0,
    sessionsCompleted: 0
  });
  const [recentActivity, setRecentActivity] = useState<RecentActivity[]>([]);
  const [error, setError] = useState<string>('');

  const { user, logout } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setIsLoading(true);
      // TODO: Implement actual API calls to fetch dashboard data
      // For now, using mock data
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      
      setStats({
        totalWords: 127,
        wordsLearned: 89,
        studyStreak: 7,
        sessionsCompleted: 23
      });

      setRecentActivity([
        {
          id: '1',
          type: 'vocabulary',
          title: 'New Words Added',
          description: 'Added 5 new Spanish words to your vocabulary',
          timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2 hours ago
        },
        {
          id: '2',
          type: 'practice',
          title: 'Practice Session Completed',
          description: 'Completed daily vocabulary practice (15 minutes)',
          timestamp: new Date(Date.now() - 6 * 60 * 60 * 1000) // 6 hours ago
        },
        {
          id: '3',
          type: 'achievement',
          title: 'Achievement Unlocked',
          description: 'Reached 7-day study streak!',
          timestamp: new Date(Date.now() - 24 * 60 * 60 * 1000) // 1 day ago
        }
      ]);
    } catch (err) {
      setError('Failed to load dashboard data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/', { replace: true });
    } catch (err) {
      setError('Failed to log out. Please try again.');
    }
  };

  const formatTimeAgo = (timestamp: Date) => {
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - timestamp.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    const diffInDays = Math.floor(diffInHours / 24);
    return `${diffInDays}d ago`;
  };

  const getActivityIcon = (type: RecentActivity['type']) => {
    switch (type) {
      case 'vocabulary':
        return '📚';
      case 'practice':
        return '🎯';
      case 'achievement':
        return '🏆';
      default:
        return '📝';
    }
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
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <span className="text-2xl font-bold text-gray-900">🗣️ Language Tracker</span>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                Welcome back, {user?.username}!
              </span>
              <Link
                to="/profile"
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Profile
              </Link>
              <button
                onClick={handleLogout}
                className="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md text-sm font-medium"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6">
            <Alert variant="error" message={error} />
          </div>
        )}

        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Good {new Date().getHours() < 12 ? 'morning' : new Date().getHours() < 17 ? 'afternoon' : 'evening'}, {user?.username}!
          </h1>
          <p className="text-gray-600">
            Ready to continue your language learning journey?
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">📚</span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Total Words</p>
                <p className="text-2xl font-bold text-gray-900">{stats.totalWords}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">✅</span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Words Learned</p>
                <p className="text-2xl font-bold text-gray-900">{stats.wordsLearned}</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">🔥</span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Study Streak</p>
                <p className="text-2xl font-bold text-gray-900">{stats.studyStreak} days</p>
              </div>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <span className="text-2xl">🎯</span>
              </div>
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-600">Sessions</p>
                <p className="text-2xl font-bold text-gray-900">{stats.sessionsCompleted}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <Link
            to="/practice"
            className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
          >
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">🎯</span>
              <h3 className="text-lg font-semibold text-gray-900">Practice Session</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Review vocabulary and practice with interactive exercises
            </p>
            <span className="text-primary-600 font-medium">Start Practice →</span>
          </Link>

          <Link
            to="/vocabulary"
            className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
          >
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">📚</span>
              <h3 className="text-lg font-semibold text-gray-900">Vocabulary</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Browse and manage your word collection
            </p>
            <span className="text-primary-600 font-medium">View Vocabulary →</span>
          </Link>

          <Link
            to="/progress"
            className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
          >
            <div className="flex items-center mb-4">
              <span className="text-2xl mr-3">📊</span>
              <h3 className="text-lg font-semibold text-gray-900">Progress</h3>
            </div>
            <p className="text-gray-600 mb-4">
              Track your learning progress and achievements
            </p>
            <span className="text-primary-600 font-medium">View Progress →</span>
          </Link>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Recent Activity</h2>
          </div>
          <div className="divide-y divide-gray-200">
            {recentActivity.length > 0 ? (
              recentActivity.map((activity) => (
                <div key={activity.id} className="px-6 py-4">
                  <div className="flex items-start">
                    <span className="text-xl mr-3 mt-1">{getActivityIcon(activity.type)}</span>
                    <div className="flex-1">
                      <h3 className="text-sm font-medium text-gray-900">{activity.title}</h3>
                      <p className="text-sm text-gray-600 mt-1">{activity.description}</p>
                      <p className="text-xs text-gray-500 mt-2">{formatTimeAgo(activity.timestamp)}</p>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <div className="px-6 py-8 text-center">
                <span className="text-4xl mb-4 block">📝</span>
                <p className="text-gray-500">No recent activity. Start learning to see your progress here!</p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
};