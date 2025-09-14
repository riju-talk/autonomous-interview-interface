// Utility functions for working with session storage

export const SESSION_KEYS = {
  INTERVIEW_SESSION: 'interview_session',
  AUTH_TOKEN: 'auth_token',
  USER_PREFERENCES: 'user_preferences',
};

// Generic storage functions
export const storage = {
  get: (key) => {
    try {
      const item = sessionStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error(`Error getting ${key} from storage:`, error);
      return null;
    }
  },
  
  set: (key, value) => {
    try {
      sessionStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error(`Error setting ${key} in storage:`, error);
      return false;
    }
  },
  
  remove: (key) => {
    try {
      sessionStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error(`Error removing ${key} from storage:`, error);
      return false;
    }
  },
  
  clear: () => {
    try {
      sessionStorage.clear();
      return true;
    } catch (error) {
      console.error('Error clearing storage:', error);
      return false;
    }
  },
};

// Interview session specific functions
export const interviewStorage = {
  saveSession: (sessionData) => {
    return storage.set(SESSION_KEYS.INTERVIEW_SESSION, {
      ...sessionData,
      _lastUpdated: new Date().toISOString(),
    });
  },
  
  getSession: () => {
    return storage.get(SESSION_KEYS.INTERVIEW_SESSION);
  },
  
  clearSession: () => {
    return storage.remove(SESSION_KEYS.INTERVIEW_SESSION);
  },
  
  // Check if there's an existing session that can be resumed
  hasActiveSession: () => {
    const session = storage.get(SESSION_KEYS.INTERVIEW_SESSION);
    if (!session) return false;
    
    // Check if session is expired (older than 24 hours)
    const lastUpdated = new Date(session._lastUpdated);
    const now = new Date();
    const hoursDiff = Math.abs(now - lastUpdated) / 36e5; // Convert ms to hours
    
    return hoursDiff < 24; // Session expires after 24 hours
  },
};

export default storage;
