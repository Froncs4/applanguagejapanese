import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { STORIES } from '../data/stories';
import { useAuth } from '../context/AuthContext';

const StoriesScreen = () => {
  const { user } = useAuth();
  const [selectedStory, setSelectedStory] = useState(null);

  // Проверка разблокировки истории
  const checkUnlock = (story) => {
    // В реальном приложении проверять user.xp или user.completedStories
    if (story.isUnlocked) return true;
    
    if (story.requirement && story.requirement.includes('XP')) {
        const reqXp = parseInt(story.requirement.match(/\d+/)[0]);
        return (user?.xp || 0) >= reqXp;
    }
    
    return false; // По умолчанию заблокировано
  };

  const handleStoryClick = (story) => {
    if (checkUnlock(story)) {
      setSelectedStory(story);
    } else {
      // Можно добавить уведомление или вибрацию
      alert(`Требование: ${story.requirement}`);
    }
  };

  if (selectedStory) {
    return (
      <StoryReader 
        story={selectedStory} 
        onClose={() => setSelectedStory(null)} 
        user={user}
      />
    );
  }

  return (
    <div className="screen active" style={{ paddingBottom: '100px' }}>
      <div className="glass-header">
        <h2 style={{ fontWeight: 800, fontSize: '26px' }}>📚 Интерактивные Истории</h2>
        <p style={{ color: 'var(--text-hint)', fontSize: '14px' }}>Погружайся в японский язык через увлекательные истории</p>
      </div>

      <div className="section">
        {STORIES.map((story) => {
          const isUnlocked = checkUnlock(story);
          return (
            <motion.div
              key={story.id}
              whileTap={{ scale: 0.98 }}
              onClick={() => handleStoryClick(story)}
              style={{
                background: 'rgba(30, 30, 46, 0.7)',
                borderRadius: '16px',
                padding: '16px',
                marginBottom: '16px',
                border: isUnlocked ? '1px solid rgba(255,255,255,0.1)' : '1px solid rgba(255,255,255,0.05)',
                position: 'relative',
                overflow: 'hidden',
                cursor: 'pointer',
                opacity: isUnlocked ? 1 : 0.7
              }}
            >
              <div style={{ display: 'flex', gap: '15px', marginBottom: '12px' }}>
                <div style={{ 
                  fontSize: '40px', 
                  background: 'rgba(0,0,0,0.2)', 
                  width: '60px', 
                  height: '60px', 
                  borderRadius: '12px', 
                  display: 'flex', 
                  alignItems: 'center', 
                  justifyContent: 'center' 
                }}>
                  {story.image}
                </div>
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '18px', fontWeight: '800', marginBottom: '6px' }}>{story.title}</div>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    <span style={{ fontSize: '11px', padding: '3px 8px', borderRadius: '8px', background: 'rgba(102, 126, 234, 0.2)', color: 'var(--primary)', fontWeight: '600' }}>{story.level}</span>
                    <span style={{ fontSize: '11px', padding: '3px 8px', borderRadius: '8px', background: 'rgba(255, 255, 255, 0.1)', color: 'var(--text-hint)', fontWeight: '600' }}>{story.difficulty}</span>
                    <span style={{ fontSize: '11px', padding: '3px 8px', borderRadius: '8px', background: 'rgba(255, 193, 7, 0.2)', color: 'var(--warning)', fontWeight: '600' }}>⏱️ {story.duration}</span>
                  </div>
                </div>
                <div style={{ fontSize: '24px' }}>
                  {isUnlocked ? '🔓' : '🔒'}
                </div>
              </div>

              <div style={{ fontSize: '14px', color: 'var(--text-hint)', marginBottom: '10px', lineHeight: '1.4' }}>
                {story.description}
              </div>

              <div style={{ 
                marginBottom: '12px', 
                padding: '8px 12px', 
                background: 'rgba(0,0,0,0.2)', 
                borderRadius: '10px', 
                borderLeft: '3px solid var(--primary)' 
              }}>
                <span style={{ color: 'var(--text-hint)', fontStyle: 'italic', fontSize: '13px' }}>"{story.preview}"</span>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '12px' }}>
                 <div style={{ color: 'var(--success)', fontWeight: 'bold' }}>+{story.xp} XP</div>
                 <div style={{ color: 'var(--text-hint)' }}>📝 {story.vocabulary.length} слов</div>
              </div>
              
              {!isUnlocked && (
                  <div style={{
                      position: 'absolute',
                      top: 0, left: 0, right: 0, bottom: 0,
                      background: 'rgba(0,0,0,0.6)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      backdropFilter: 'blur(2px)'
                  }}>
                      <div style={{ background: 'var(--error)', padding: '6px 12px', borderRadius: '8px', fontWeight: 'bold', fontSize: '12px' }}>
                          {story.requirement}
                      </div>
                  </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};

const StoryReader = ({ story, onClose, user }) => {
    // Если у истории есть stages, используем их, иначе создаем один этап из content/quiz
    const stages = story.stages || [{
        id: 'single',
        title: story.title,
        content: story.content,
        quiz: story.quiz
    }];

    const [currentStageIndex, setCurrentStageIndex] = useState(0);
    const [showQuiz, setShowQuiz] = useState(false);
    const [quizResult, setQuizResult] = useState(null); // null, 'correct', 'wrong'

    const currentStage = stages[currentStageIndex];
    if (!currentStage) return null;

    const handleWordClick = (word) => {
        if (word.interactive) {
            // Можно добавить модалку с переводом
            console.log(word);
        }
    };

    const handleQuizAnswer = (option) => {
        if (option === currentStage.quiz.correct) {
            setQuizResult('correct');
        } else {
            setQuizResult('wrong');
        }
    };

    const nextStage = () => {
        setQuizResult(null);
        setShowQuiz(false);
        if (currentStageIndex < stages.length - 1) {
            setCurrentStageIndex(prev => prev + 1);
        } else {
            // Конец истории
            onClose();
            // TODO: Отправить результат на сервер
            alert(`История завершена! +${story.xp} XP`);
        }
    };

    return (
        <div className="screen active" style={{ paddingBottom: '0', height: '100vh', display: 'flex', flexDirection: 'column' }}>
            <div className="glass-header" style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'white', fontSize: '24px' }}>←</button>
                <div style={{ flex: 1 }}>
                    <div style={{ fontSize: '12px', color: 'var(--text-hint)' }}>{story.title}</div>
                    <div style={{ fontWeight: 'bold' }}>{currentStage.title || 'Чтение'}</div>
                </div>
                <div style={{ fontSize: '12px', background: 'rgba(255,255,255,0.1)', padding: '4px 8px', borderRadius: '10px' }}>
                    {currentStageIndex + 1}/{stages.length}
                </div>
            </div>

            <div style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
                {!showQuiz ? (
                    <div style={{ background: 'rgba(30, 30, 46, 0.5)', padding: '20px', borderRadius: '16px', lineHeight: '2.5', fontSize: '18px' }}>
                        {currentStage.content.map((word, idx) => (
                            <span 
                                key={idx}
                                onClick={() => handleWordClick(word)}
                                style={{ 
                                    marginRight: '4px', 
                                    cursor: word.interactive ? 'pointer' : 'default',
                                    color: word.interactive ? 'var(--primary)' : 'white',
                                    borderBottom: word.interactive ? '1px dashed rgba(102, 126, 234, 0.5)' : 'none',
                                    position: 'relative',
                                    display: 'inline-block'
                                }}
                            >
                                <ruby>
                                    {word.jp}
                                    <rt style={{ color: 'var(--text-hint)', fontSize: '10px' }}>{word.kana}</rt>
                                </ruby>
                            </span>
                        ))}
                    </div>
                ) : (
                    <div style={{ background: 'rgba(30, 30, 46, 0.5)', padding: '20px', borderRadius: '16px' }}>
                        <h3 style={{ marginBottom: '20px', textAlign: 'center' }}>{currentStage.quiz.question}</h3>
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                            {currentStage.quiz.options.map((opt, idx) => (
                                <button
                                    key={idx}
                                    onClick={() => handleQuizAnswer(opt)}
                                    disabled={quizResult === 'correct'}
                                    style={{
                                        padding: '15px',
                                        borderRadius: '12px',
                                        border: 'none',
                                        background: quizResult === 'correct' && opt === currentStage.quiz.correct 
                                            ? 'var(--success)' 
                                            : quizResult === 'wrong' && opt !== currentStage.quiz.correct // Просто подсветка ошибки
                                                ? 'rgba(255,255,255,0.1)' 
                                                : 'rgba(255,255,255,0.1)',
                                        color: 'white',
                                        fontSize: '16px',
                                        cursor: 'pointer',
                                        textAlign: 'left'
                                    }}
                                >
                                    {opt}
                                </button>
                            ))}
                        </div>
                        {quizResult === 'correct' && (
                            <div style={{ marginTop: '20px', textAlign: 'center', color: 'var(--success)', fontWeight: 'bold' }}>
                                Правильно! 🎉
                            </div>
                        )}
                         {quizResult === 'wrong' && (
                            <div style={{ marginTop: '20px', textAlign: 'center', color: 'var(--error)', fontWeight: 'bold' }}>
                                Попробуй еще раз! <br/>
                                <span style={{fontSize: '12px', color: 'var(--text-hint)'}}>Подсказка: {currentStage.quiz.hint}</span>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div style={{ padding: '20px' }}>
                {!showQuiz ? (
                    <button 
                        className="btn-primary" 
                        style={{ width: '100%', padding: '16px', borderRadius: '16px', border: 'none', background: 'var(--primary)', color: 'white', fontSize: '16px', fontWeight: 'bold' }}
                        onClick={() => setShowQuiz(true)}
                    >
                        Далее
                    </button>
                ) : (
                    <button 
                         className="btn-primary" 
                         style={{ width: '100%', padding: '16px', borderRadius: '16px', border: 'none', background: quizResult === 'correct' ? 'var(--success)' : 'gray', color: 'white', fontSize: '16px', fontWeight: 'bold' }}
                         onClick={nextStage}
                         disabled={quizResult !== 'correct'}
                    >
                        {currentStageIndex < stages.length - 1 ? 'Следующая часть' : 'Завершить'}
                    </button>
                )}
            </div>
        </div>
    );
};

export default StoriesScreen;
