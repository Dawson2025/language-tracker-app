// resource_id: 0bd1cf55-15e3-4d64-b1fa-6aaa7667bf32
/**
 * Vocabulary Service
 * Language Tracker Vocabulary Management Feature
 * 
 * Frontend API client for vocabulary operations.
 * Manages words, categories, and learning progress.
 */

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

// Types for vocabulary management
export interface Word {
  id: number;
  word: string;
  translation: string;
  language: string;
  target_language: string;
  category?: string;
  difficulty_level: 'beginner' | 'intermediate' | 'advanced';
  pronunciation?: string;
  example_sentence?: string;
  example_translation?: string;
  notes?: string;
  created_at: string;
  updated_at: string;
  learning_progress: WordProgress;
}

export interface WordProgress {
  id: number;
  word_id: number;
  user_id: number;
  mastery_level: number; // 0-100
  last_reviewed: string | null;
  review_count: number;
  correct_count: number;
  incorrect_count: number;
  next_review: string | null;
  is_mastered: boolean;
  created_at: string;
  updated_at: string;
}

export interface Category {
  id: number;
  name: string;
  description?: string;
  color?: string;
  created_at: string;
  word_count: number;
}

export interface AddWordRequest {
  word: string;
  translation: string;
  language: string;
  target_language: string;
  category?: string;
  difficulty_level?: 'beginner' | 'intermediate' | 'advanced';
  pronunciation?: string;
  example_sentence?: string;
  example_translation?: string;
  notes?: string;
}

export interface UpdateWordRequest extends Partial<AddWordRequest> {
  id: number;
}

export interface WordFilters {
  language?: string;
  target_language?: string;
  category?: string;
  difficulty_level?: string;
  mastery_level?: 'not-started' | 'learning' | 'mastered';
  search?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  page: number;
  pages: number;
  per_page: number;
  total: number;
  has_next: boolean;
  has_prev: boolean;
}

// HTTP client for API calls
class APIClient {
  private getAuthHeaders(): Record<string, string> {
    const token = localStorage.getItem('auth_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...this.getAuthHeaders(),
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || `HTTP ${response.status}`);
    }

    return await response.json();
  }

  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' });
  }

  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// Vocabulary service implementation
class VocabularyService {
  private client: APIClient;

  constructor() {
    this.client = new APIClient();
  }

  // Words management
  async getWords(
    page: number = 1,
    per_page: number = 20,
    filters?: WordFilters
  ): Promise<PaginatedResponse<Word>> {
    const params = new URLSearchParams();
    params.append('page', page.toString());
    params.append('per_page', per_page.toString());
    
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });
    }

    return await this.client.get<PaginatedResponse<Word>>(`/vocabulary/words?${params}`);
  }

  async getWord(wordId: number): Promise<Word> {
    return await this.client.get<Word>(`/vocabulary/words/${wordId}`);
  }

  async addWord(wordData: AddWordRequest): Promise<Word> {
    return await this.client.post<Word>('/vocabulary/words', wordData);
  }

  async updateWord(wordData: UpdateWordRequest): Promise<Word> {
    const { id, ...updateData } = wordData;
    return await this.client.put<Word>(`/vocabulary/words/${id}`, updateData);
  }

  async deleteWord(wordId: number): Promise<{ success: boolean; message: string }> {
    return await this.client.delete(`/vocabulary/words/${wordId}`);
  }

  // Categories management
  async getCategories(): Promise<Category[]> {
    return await this.client.get<Category[]>('/vocabulary/categories');
  }

  async createCategory(name: string, description?: string, color?: string): Promise<Category> {
    return await this.client.post<Category>('/vocabulary/categories', {
      name,
      description,
      color
    });
  }

  async updateCategory(
    categoryId: number,
    updates: { name?: string; description?: string; color?: string }
  ): Promise<Category> {
    return await this.client.put<Category>(`/vocabulary/categories/${categoryId}`, updates);
  }

  async deleteCategory(categoryId: number): Promise<{ success: boolean; message: string }> {
    return await this.client.delete(`/vocabulary/categories/${categoryId}`);
  }

  // Learning progress
  async updateWordProgress(
    wordId: number,
    isCorrect: boolean
  ): Promise<WordProgress> {
    return await this.client.post<WordProgress>(`/vocabulary/words/${wordId}/progress`, {
      is_correct: isCorrect
    });
  }

  async getWordProgress(wordId: number): Promise<WordProgress> {
    return await this.client.get<WordProgress>(`/vocabulary/words/${wordId}/progress`);
  }

  async resetWordProgress(wordId: number): Promise<WordProgress> {
    return await this.client.post<WordProgress>(`/vocabulary/words/${wordId}/progress/reset`);
  }

  // Learning sessions
  async getWordsForReview(limit: number = 10): Promise<Word[]> {
    return await this.client.get<Word[]>(`/vocabulary/review?limit=${limit}`);
  }

  async getWordsForPractice(
    filters?: { 
      category?: string; 
      difficulty_level?: string; 
      limit?: number;
    }
  ): Promise<Word[]> {
    const params = new URLSearchParams();
    if (filters) {
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value.toString());
      });
    }

    return await this.client.get<Word[]>(`/vocabulary/practice?${params}`);
  }

  // Statistics
  async getVocabularyStats(): Promise<{
    total_words: number;
    words_learned: number;
    words_mastered: number;
    learning_streak: number;
    categories_count: number;
    average_mastery: number;
  }> {
    return await this.client.get('/vocabulary/stats');
  }

  // Bulk operations
  async importWords(words: AddWordRequest[]): Promise<{
    success: number;
    failed: number;
    errors: string[];
  }> {
    return await this.client.post('/vocabulary/import', { words });
  }

  async exportWords(format: 'json' | 'csv' = 'json'): Promise<Blob> {
    const response = await fetch(`${API_BASE_URL}/vocabulary/export?format=${format}`, {
      headers: this.client['getAuthHeaders'](),
    });

    if (!response.ok) {
      throw new Error('Export failed');
    }

    return await response.blob();
  }
}

// Export singleton instance
export const vocabularyService = new VocabularyService();

export default vocabularyService;