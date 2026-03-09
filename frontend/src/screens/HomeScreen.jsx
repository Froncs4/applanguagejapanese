import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const HomeScreen = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [leagueTimeLeft, setLeagueTimeLeft] = useState('');
  
  if (!user) return <div style={{padding: '20px', textAlign: 'center'}}>Загрузка профиля...</div>;

  // Таймер до конца недели (Воскресенье 23:59:59)
  useEffect(() => {
    const updateTimer = () => {
      const now = new Date();
      const endOfWeek = new Date();
      // Устанавливаем на следующее воскресенье
      endOfWeek.setDate(now.getDate() + (7 - now.getDay())); 
      endOfWeek.setHours(23, 59, 59, 999);
      
      const diff = endOfWeek - now;
      if (diff <= 0) {
        setLeagueTimeLeft('Обновление...');
        return;
      }
      
      const hours = Math.floor(diff / (1000 * 60 * 60));
      const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
      
      setLeagueTimeLeft(`${hours}ч ${minutes}м`);
    };

    updateTimer();
    const interval = setInterval(updateTimer, 60000); // Обновляем раз в минуту
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="screen active">
      {/* Шапка профиля */}
      <div className="glass-header" style={{ paddingBottom: '40px' }}>
        <div className="user-row" style={{ justifyContent: 'center', marginBottom: '10px' }}>
          <div className="avatar" style={{ backgroundImage: `url(https://api.dicebear.com/7.x/adventurer/svg?seed=${user.username})` }}></div>
          <div className="user-info" style={{ textAlign: 'left' }}>
            <h1>Привет, {user.username}! 👋</h1>
            <div className="user-rank">
              🏆 {user.league} Лига
            </div>
          </div>
        </div>
        
        {/* Статистика */}
        <div className="stats-row">
          <div className="stat-box">
            <div className="stat-value">🔥 {user.streak}</div>
            <div className="stat-label">Дней подряд</div>
          </div>
          <div className="stat-box">
            <div className="stat-value">⚡ {user.todayXp}</div>
            <div className="stat-label">XP сегодня</div>
          </div>
        </div>
      </div>

      <div className="section" style={{ marginTop: '-20px' }}>
        <h3 className="section-title">🎯 Ежедневные цели</h3>
        
        {/* Кнопка для начала обучения (если нет прогресса) */}
        {user.xp < 50 && (
          <div 
            onClick={() => navigate('/alphabet')}
            style={{
              background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
              borderRadius: '16px',
              padding: '20px',
              marginBottom: '20px',
              display: 'flex',
              alignItems: 'center',
              gap: '15px',
              cursor: 'pointer',
              boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)'
            }}
          >
            <div style={{ fontSize: '32px' }}>🚀</div>
            <div>
              <div style={{ fontWeight: 'bold', fontSize: '18px', marginBottom: '4px' }}>Начать обучение</div>
              <div style={{ fontSize: '13px', opacity: 0.9 }}>Выучи первые символы хираганы!</div>
            </div>
          </div>
        )}

        <div className="quest-item">
          <div className="quest-icon">📚</div>
          <div className="quest-info">
            <div className="quest-title">Изучить 5 слов</div>
            <div className="quest-bar"><div className="quest-bar-fill" style={{ width: '40%' }}></div></div>
          </div>
          <div className="quest-reward">+50 XP</div>
        </div>
        <div className="quest-item done">
          <div className="quest-icon">⚡</div>
          <div className="quest-info">
            <div className="quest-title">Заработать 20 XP</div>
            <div className="quest-bar"><div className="quest-bar-fill" style={{ width: '100%' }}></div></div>
          </div>
          <div className="quest-reward">✅</div>
        </div>
      </div>

      <div className="section">
        <h3 className="section-title">🏆 Лига</h3>
        <div style={{ background: 'rgba(0,0,0,0.3)', borderRadius: '16px', padding: '16px', display: 'flex', alignItems: 'center', gap: '15px' }}>
          <div style={{ fontSize: '30px' }}>🛡️</div>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: '14px', fontWeight: 'bold', marginBottom: '4px' }}>До следующей лиги</div>
            <div style={{ fontSize: '12px', color: 'var(--text-hint)' }}>{user.nextLeagueXp - user.xp} XP осталось</div>
          </div>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '12px', color: 'var(--warning)', fontWeight: 'bold' }}>⏳ {leagueTimeLeft}</div>
            <div style={{ fontSize: '10px', color: 'var(--text-hint)' }}>до конца</div>
          </div>
        </div>
      </div>

      <div className="section" style={{ paddingBottom: '100px' }}>
        <h3 className="section-title">Быстрый доступ</h3>
        <div className="menu-grid">
          <motion.div whileTap={{ scale: 0.95 }} className="menu-card wide" onClick={() => navigate('/learn')}>
            <div className="card-icon">🎓</div>
            <div>
              <div className="card-title">Начать урок</div>
              <div className="card-subtitle">Продолжить N5</div>
            </div>
          </motion.div>
          <motion.div whileTap={{ scale: 0.95 }} className="menu-card" onClick={() => navigate('/wheel')}>
            <div className="card-icon">🎡</div>
            <div className="card-title">Рулетка</div>
          </motion.div>
          <motion.div whileTap={{ scale: 0.95 }} className="menu-card" onClick={() => navigate('/shop')}>
            <div className="card-icon">🛍️</div>
            <div className="card-title">Магазин</div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default HomeScreen;