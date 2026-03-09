import { useState, useCallback } from 'react';
import { apiFetch } from '../utils/api';

export const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const request = useCallback(async (endpoint, options = {}) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch(endpoint, options);
      return data;
    } catch (err) {
      setError(err.message || 'API Error');
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { loading, error, request };
};
