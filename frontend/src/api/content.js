import request from "./request";

export const getSocialLinks = () => request.get("/api/content/social-links");
export const getTechStacks = () => request.get("/api/content/tech-stacks");
export const getLearningNodes = () => request.get("/api/content/learning");
export const getLibraryItems = (params = {}) => request.get("/api/content/library", { params });
export const getAlbums = () => request.get("/api/content/albums");
export const getGuestbook = () => request.get("/api/content/guestbook");
export const createGuestbookMessage = (data) => request.post("/api/content/guestbook", data);
export const getChangelog = () => request.get("/api/content/changelog");

const adminBase = "/api/admin/content";

export const getAdminResource = (resource) => request.get(`${adminBase}/${resource}`);
export const getAdminLibrary = (params = {}) => request.get(`${adminBase}/library`, { params });
export const createAdminResource = (resource, data) => request.post(`${adminBase}/${resource}`, data);
export const updateAdminResource = (resource, id, data) => request.patch(`${adminBase}/${resource}/${id}`, data);
export const deleteAdminResource = (resource, id) => request.delete(`${adminBase}/${resource}/${id}`);
export const addAlbumPhoto = (albumId, data) => request.post(`${adminBase}/albums/${albumId}/photos`, data);
export const deleteAlbumPhoto = (photoId) => request.delete(`${adminBase}/photos/${photoId}`);
