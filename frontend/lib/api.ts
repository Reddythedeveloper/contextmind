import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
});

export const uploadDocument = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const { data } = await api.post('/documents/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return data;
};

export const searchDocuments = async (query: string) => {
  const { data } = await api.get(`/documents/search?q=${query}`);
  return data;
};

export const getPersona = async () => {
  const { data } = await api.get('/users/persona');
  return data;
};

export const updatePersona = async (update: { expertise_level?: string; response_style?: string; interests?: string[] }) => {
  const { data } = await api.post('/users/persona', update);
  return data;
};

export const getDocuments = async (sessionId: string) => {
  const { data } = await api.get(`/documents/?session_id=${sessionId}`);
  return data;
};

export const listSessions = async () => {
  const { data } = await api.get('/chat/sessions');
  return data;
};

export const deleteSession = async (sessionId: string) => {
  const { data } = await api.delete(`/chat/sessions/${sessionId}`);
  return data;
};
