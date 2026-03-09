import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { Header } from './components/Header';
import { BottomNav } from './components/BottomNav';
import HomeScreen from './screens/HomeScreen';
import AlphabetScreen from './screens/AlphabetScreen';
import StoriesScreen from './screens/StoriesScreen';
import GrammarScreen from './screens/GrammarScreen';
import './App.css';

function App() {
  const { user, loading } = useAuth();
  
  if (loading) return (
    <div style={{
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh', 
      color: '#fff'
    }}>
      Загрузка...
    </div>
  );

  return (
    <div className="app-container">
      {/* Шапка отображается, если пользователь загружен */}
      {user && <Header isOnline={true} coins={user.coins || 0} />}
      
      <main className="content">
        <Routes>
          <Route path="/" element={<HomeScreen />} />
          <Route path="/alphabet" element={<AlphabetScreen />} />
          <Route path="/stories" element={<StoriesScreen />} />
          <Route path="/grammar" element={<GrammarScreen />} />
          
          {/* Заглушки для остальных маршрутов */}
          <Route path="/shop" element={
            <div style={{padding: 20, textAlign: 'center', color: 'var(--text-hint)'}}>
              <h2>🛍️ Магазин</h2>
              <p>Скоро открытие!</p>
            </div>
          } />
          
          <Route path="*" element={
            <div style={{padding: 20, textAlign: 'center'}}>
              <h2>404</h2>
              <p>Страница не найдена</p>
            </div>
          } />
        </Routes>
      </main>
      
      <BottomNav />
    </div>
  );
}

export default App;
