import React, { createContext, useState, useEffect, useContext } from 'react';
import { apiFetch, checkApiAvailability } from '../utils/api';

const AuthContext = createContext();

export const useAuth = () => {
  return useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchUser = async () => {
    try {
      setLoading(true);
      // Проверка API перед запросом
      const isApiOk = await checkApiAvailability();
      
      if (!isApiOk) {
        // Если API недоступен, используем мок-данные для разработки
        console.warn('API unavailable, using mock user');
        setUser({
          id: 'mock_user',
          username: 'Student (Offline)',
          league: 'Бронзовая',
          xp: 120,
          nextLeagueXp: 500,
          streak: 5,
          todayXp: 30,
          coins: 100,
          cardsLearned: 15
        });
        setLoading(false);
        return;
      }

      // Запрос пользователя
      const data = await apiFetch('/api/user');
      if (data && data.success) {
        setUser({
          id: data.user.id,
          username: data.user.name || 'Student',
          league: data.user.league || 'Бронзовая',
          xp: data.user.xp || 0,
          nextLeagueXp: 500, // Это значение может приходить с бэка или рассчитываться
          streak: data.user.streak || 0,
          todayXp: 0, // Нужно получать отдельно или считать
          coins: data.user.coins || 0,
          cardsLearned: data.user.cards_learned || 0
        });
        
        // Дополнительный запрос статистики если нужно
        // const stats = await apiFetch('/api/user/stats');
        // if (stats) { ... }

      } else {
        setError('Failed to fetch user data');
      }
    } catch (err) {
      console.error('Auth fetch error:', err);
      setError(err.message);
      // Fallback user on error
      setUser({
        id: 'error_user',
        username: 'Guest',
        league: 'Novice',
        xp: 0,
        nextLeagueXp: 100,
        streak: 0,
        todayXp: 0
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
  }, []);

  const value = {
    user,
    loading,
    error,
    refreshUser: fetchUser
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};
