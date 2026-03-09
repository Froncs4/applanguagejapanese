import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, BookOpen, MessageSquare, ShoppingBag, Trophy } from 'lucide-react';

export const BottomNav = () => {
  return (
    <div className="bottom-nav">
      <NavLink to="/" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <Home className="icon" size={24} />
        <span>Главная</span>
      </NavLink>
      
      <NavLink to="/alphabet" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <BookOpen className="icon" size={24} />
        <span>Азбука</span>
      </NavLink>
      
      <NavLink to="/stories" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <MessageSquare className="icon" size={24} />
        <span>Истории</span>
      </NavLink>
      
      <NavLink to="/grammar" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <Trophy className="icon" size={24} />
        <span>Правила</span>
      </NavLink>
      
      <NavLink to="/shop" className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}>
        <ShoppingBag className="icon" size={24} />
        <span>Магазин</span>
      </NavLink>
    </div>
  );
};