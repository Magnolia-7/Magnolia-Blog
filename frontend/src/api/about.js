import request from './request';

export function getAbout() {
  return request.get('/api/about');
}

export function getAdminAbout(data) {
  return request.get('/api/admin/about');
}

export function updateAdminAbout(data) {
  return request.patch('/api/admin/about', data);
}