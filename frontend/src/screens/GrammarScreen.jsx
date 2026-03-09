import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GRAMMAR_N5 } from '../data/grammar';
import { useContent } from '../hooks/useContent';

const GrammarScreen = () => {
  const { content } = useContent();
  const [selectedPointId, setSelectedPointId] = useState(null);

  // Используем данные из хука (если есть), иначе фолбэк
  const grammarList = (content?.grammar_n5 && content.grammar_n5.length > 0) 
    ? content.grammar_n5 
    : GRAMMAR_N5;

  return (
    <div className="screen active" style={{ paddingBottom: '100px' }}>
      <div className="glass-header">
        <h2 style={{ fontWeight: 800, fontSize: '26px' }}>🏆 Грамматика</h2>
        <p style={{ color: 'var(--text-hint)', fontSize: '14px' }}>Основные правила N5</p>
      </div>

      <div className="section">
        {grammarList.map((point, index) => {
          const pointId = point.id || `g-${index}`;
          const isSelected = selectedPointId === pointId;
          
          return (
            <motion.div
              key={pointId}
              layout="position"
              onClick={() => setSelectedPointId(isSelected ? null : pointId)}
              style={{
                background: 'rgba(30, 30, 46, 0.7)',
                borderRadius: '16px',
                padding: '16px',
                marginBottom: '12px',
                border: '1px solid rgba(255,255,255,0.05)',
                cursor: 'pointer',
                overflow: 'hidden'
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ fontWeight: 'bold', fontSize: '18px', color: 'var(--primary)' }}>
                  {point.title}
                </div>
                <motion.div 
                  animate={{ rotate: isSelected ? 180 : 0 }}
                  transition={{ duration: 0.3 }}
                >
                  ▼
                </motion.div>
              </div>
              
              <div style={{ fontSize: '12px', color: 'var(--text-hint)', marginTop: '4px' }}>
                {point.structure}
              </div>

              <AnimatePresence>
                {isSelected && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <div style={{ marginTop: '12px', paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.1)' }}>
                      <p style={{ fontSize: '14px', lineHeight: '1.5', marginBottom: '12px' }}>
                        {point.description}
                      </p>
                      
                      {point.examples && point.examples.map((ex, i) => (
                        <div key={i} style={{ 
                          background: 'rgba(0,0,0,0.2)', 
                          padding: '10px', 
                          borderRadius: '8px',
                          marginBottom: '8px',
                          borderLeft: '3px solid var(--accent)'
                        }}>
                          <div style={{ fontSize: '16px', marginBottom: '4px' }}>{ex.japanese}</div>
                          <div style={{ fontSize: '12px', color: 'var(--text-hint)' }}>{ex.reading}</div>
                          <div style={{ fontSize: '14px', marginTop: '4px' }}>{ex.translation}</div>
                        </div>
                      ))}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

export default GrammarScreen;
