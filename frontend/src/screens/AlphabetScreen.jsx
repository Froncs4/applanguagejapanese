import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { KANA_CHARTS } from '../data/kana';

const AlphabetScreen = () => {
  const [activeTab, setActiveTab] = useState('hiragana');
  const [selectedChar, setSelectedChar] = useState(null);

  // Воспроизведение звука (пока заглушка)
  const playSound = (romaji) => {
    if (!romaji) return;
    console.log(`Playing sound for: ${romaji}`);
    // new Audio(`/assets/sounds/${romaji}.mp3`).play().catch(() => {});
  };

  return (
    <div className="screen active" style={{ paddingBottom: '100px' }}>
      <div className="glass-header">
        <h2 style={{ fontWeight: 800, fontSize: '26px' }}>🎌 Азбука</h2>
        <p style={{ color: 'var(--text-hint)', fontSize: '14px' }}>Хирагана и Катакана</p>
      </div>

      <div className="section">
        {/* Переключатель вкладок */}
        <div style={{ 
          display: 'flex', 
          background: 'rgba(0,0,0,0.3)', 
          borderRadius: '16px', 
          padding: '4px', 
          marginBottom: '20px' 
        }}>
          <button 
            className="btn" 
            style={{ 
              flex: 1, 
              background: activeTab === 'hiragana' ? 'var(--primary)' : 'transparent',
              color: activeTab === 'hiragana' ? 'white' : 'var(--text-hint)',
              fontSize: '14px'
            }}
            onClick={() => setActiveTab('hiragana')}
          >
            Хирагана (あ)
          </button>
          <button 
            className="btn" 
            style={{ 
              flex: 1, 
              background: activeTab === 'katakana' ? 'var(--secondary)' : 'transparent',
              color: activeTab === 'katakana' ? 'white' : 'var(--text-hint)',
              fontSize: '14px'
            }}
            onClick={() => setActiveTab('katakana')}
          >
            Катакана (ア)
          </button>
        </div>

        {/* Сетка символов */}
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(5, 1fr)', 
          gap: '8px' 
        }}>
          {KANA_CHARTS[activeTab].map((item, index) => (
            <motion.div
              key={`${activeTab}-${index}`}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.01 }}
              onClick={() => {
                if (item.char) {
                  setSelectedChar(item);
                  playSound(item.romaji);
                }
              }}
              style={{
                aspectRatio: '1',
                background: item.char ? 'rgba(30, 30, 46, 0.7)' : 'transparent',
                borderRadius: '12px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                border: item.char ? '1px solid rgba(255,255,255,0.1)' : 'none',
                cursor: item.char ? 'pointer' : 'default'
              }}
            >
              {item.char && (
                <>
                  <div style={{ fontSize: '20px', fontWeight: 'bold' }} className="japanese">
                    {item.char}
                  </div>
                  <div style={{ fontSize: '10px', color: 'var(--text-hint)' }}>
                    {item.romaji}
                  </div>
                </>
              )}
            </motion.div>
          ))}
        </div>
      </div>

      {/* Модалка с деталями (при клике) */}
      <AnimatePresence>
        {selectedChar && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            style={{
              position: 'fixed',
              top: 0, left: 0, right: 0, bottom: 0,
              background: 'rgba(0,0,0,0.8)',
              zIndex: 9999,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              backdropFilter: 'blur(5px)'
            }}
            onClick={() => setSelectedChar(null)}
          >
            <motion.div
              initial={{ scale: 0.5, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.5, y: 50 }}
              style={{
                background: 'var(--bg-secondary)',
                padding: '40px',
                borderRadius: '30px',
                textAlign: 'center',
                width: '80%',
                maxWidth: '300px',
                border: '1px solid var(--primary)',
                boxShadow: '0 0 30px rgba(102, 126, 234, 0.3)'
              }}
              onClick={(e) => e.stopPropagation()}
            >
              <div style={{ 
                fontSize: '80px', 
                marginBottom: '10px',
                background: 'linear-gradient(45deg, var(--primary), var(--accent))',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }} className="japanese">
                {selectedChar.char}
              </div>
              <div style={{ fontSize: '24px', color: 'var(--text-hint)', marginBottom: '20px' }}>
                {selectedChar.romaji}
              </div>
              <button 
                className="btn" 
                style={{ width: '100%' }}
                onClick={() => playSound(selectedChar.romaji)}
              >
                🔊 Прослушать
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default AlphabetScreen;