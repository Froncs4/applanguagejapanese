import { useState, useEffect, useCallback } from 'react';
import { apiFetch } from '../utils/api';

const CACHE_KEY = 'japanese_content_v1';

export const useContent = () => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchFromApi = useCallback(async (isBackground = false) => {
    if (!isBackground) setLoading(true);
    
    try {
      // Запрашиваем категории параллельно
      const categories = ['kanji_n5', 'words_n5', 'grammar_n5'];
      
      const results = await Promise.all(
        categories.map(async (cat) => {
          try {
             const data = await apiFetch(`/api/content?category=${cat}`);
             return { [cat]: data };
          } catch (e) {
             console.warn(`Failed to fetch ${cat}`, e);
             return { [cat]: [] };
          }
        })
      );
      
      // Объединяем результаты в один объект
      const newContent = results.reduce((acc, curr) => ({ ...acc, ...curr }), {});

      setContent(newContent);
      localStorage.setItem(CACHE_KEY, JSON.stringify(newContent));
      
    } catch (err) {
      console.error('Content fetch error:', err);
      if (!isBackground) setError(err.message);
    } finally {
      if (!isBackground) setLoading(false);
    }
  }, []);

  const loadContent = useCallback(async (forceUpdate = false) => {
    setLoading(true);
    setError(null);
    
    try {
      // 1. Пробуем загрузить из кэша
      if (!forceUpdate) {
        const cached = localStorage.getItem(CACHE_KEY);
        if (cached) {
          try {
            const parsed = JSON.parse(cached);
            setContent(parsed);
            // Фоново обновляем кэш
            fetchFromApi(true); 
            setLoading(false);
            return;
          } catch (e) {
            console.warn('Cache parse error', e);
            localStorage.removeItem(CACHE_KEY);
          }
        }
      }

      // 2. Загружаем с API если кэша нет или forceUpdate
      await fetchFromApi(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  }, [fetchFromApi]);

  useEffect(() => {
    loadContent();
  }, [loadContent]);

  return { content, loading, error, refresh: () => loadContent(true) };
};
