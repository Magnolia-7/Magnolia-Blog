import request from "./request";

export function getPosts(params = {}){
  return request.get('/api/posts/', { params });
}

export function getPostDetail(id){
  return request.get(`/api/posts/${id}/`);
}

export function searchPosts(params = {}){
  return request.get('/api/search/', { params });
}

export function getAdminPosts() {
  return request.get("/api/admin/posts");
}

export function createAdminPost(data) {
  return request.post("/api/admin/posts", data);
}

export function updateAdminPost(id, data) {
  return request.patch(`/api/admin/posts/${id}`, data);
}

export function deleteAdminPost(id) {
  return request.delete(`/api/admin/posts/${id}`);
}
