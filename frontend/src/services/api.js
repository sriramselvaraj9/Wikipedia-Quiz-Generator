import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const generateQuiz = async (url, forceRegenerate = false, storeRawHtml = false) => {
  const response = await api.post('/api/generate-quiz', {
    url,
    force_regenerate: forceRegenerate,
    store_raw_html: storeRawHtml,
  });
  return response.data;
};

export const getQuizHistory = async () => {
  const response = await api.get('/api/history');
  return response.data;
};

export const getQuizById = async (id) => {
  const response = await api.get(`/api/quiz/${id}`);
  return response.data;
};

export const deleteQuiz = async (id) => {
  const response = await api.delete(`/api/quiz/${id}`);
  return response.data;
};

export default api;
