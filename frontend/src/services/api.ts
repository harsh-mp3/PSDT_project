import axios from 'axios';
export const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api', timeout: 8000 });
api.interceptors.response.use(r => r, e => { const message = e.response?.data?.detail || e.message || 'API connection failed'; return Promise.reject(new Error(message)); });
export const get = async <T,>(path:string):Promise<T> => (await api.get<T>(path)).data;
export const post = async <T,>(path:string,data:unknown):Promise<T> => (await api.post<T>(path,data)).data;
export const put = async <T,>(path:string,data:unknown):Promise<T> => (await api.put<T>(path,data)).data;
