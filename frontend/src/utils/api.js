// Список API endpoints (можно расширить или брать из env)
const API_ENDPOINTS = [
  'https://endless-max-jowly.ngrok-free.dev',
  'https://your-backup-server.herokuapp.com',
  'https://another-backup-server.glitch.me',
  // Локальный сервер для разработки
  'http://localhost:8000'
];

let API_BASE = API_ENDPOINTS[0];
let apiAvailable = false;

// Получение данных авторизации из Telegram WebApp
const getAuthHeader = () => {
  if (window.Telegram?.WebApp?.initData) {
    return window.Telegram.WebApp.initData;
  }
  // Для разработки можно вернуть мок, если нужно
  return ''; 
};

export const checkApiAvailability = async () => {
  console.log('Checking API availability...');
  
  for (let i = 0; i < API_ENDPOINTS.length; i++) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 3000);
      
      const response = await fetch(`${API_ENDPOINTS[i]}/api/health`, {
        method: 'GET',
        headers: { 'ngrok-skip-browser-warning': 'true' },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (response.ok) {
        API_BASE = API_ENDPOINTS[i];
        apiAvailable = true;
        console.log(`Connected to API: ${API_BASE}`);
        return true;
      }
    } catch (e) {
      console.warn(`API ${API_ENDPOINTS[i]} unavailable:`, e.message);
    }
  }
  
  apiAvailable = false;
  console.warn('All API endpoints failed');
  return false;
};

// Базовая функция для запросов с авторизацией
export const apiFetch = async (endpoint, options = {}) => {
  if (!apiAvailable) {
    const isAvailable = await checkApiAvailability();
    if (!isAvailable) {
      throw new Error('API unavailable');
    }
  }

  const authHeader = getAuthHeader();
  const headers = {
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true',
    ...(authHeader ? { 'X-Telegram-Init-Data': authHeader } : {}),
    ...options.headers,
  };

  const url = `${API_BASE}${endpoint}`;
  
  try {
    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
        // Обработка 401 и других ошибок
        if (response.status === 401) {
            console.error('Unauthorized');
        }
        throw new Error(`API Error: ${response.status}`);
    }

    // Если ответ пустой (например 204), не парсим JSON
    if (response.status === 204) return null;

    return await response.json();
  } catch (error) {
    console.error(`Fetch error for ${url}:`, error);
    throw error;
  }
};

export const getApiBase = () => API_BASE;
