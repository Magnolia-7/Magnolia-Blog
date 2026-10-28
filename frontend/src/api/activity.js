import request from './request';

export const getSiteSettings = () => request.get('/api/activity/site');
export const saveSiteSettings = (data) => request.put('/api/admin/activity/site', data);
export const getSiteStats = () => request.get('/api/activity/stats');
export const recordVisit = (data) => request.post('/api/activity/visits', data);
export const getTimeLogs = (month) => request.get('/api/activity/time-logs', { params: { month } });
export const getTimeSummary = (period) => request.get('/api/activity/time-summary', { params: { period } });
export const getAdminTimeLog = (date) => request.get(`/api/admin/activity/time-logs/${date}`);
export const saveTimeLog = (date, data) => request.put(`/api/admin/activity/time-logs/${date}`, data);
export const deleteTimeLog = (date) => request.delete(`/api/admin/activity/time-logs/${date}`);
