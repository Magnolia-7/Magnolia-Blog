import request from "./request";

export function uploadImage(file, onUploadProgress) {
  const data = new FormData();
  data.append("file", file);
  return request.post("/api/admin/media/images", data, {
    headers: { "Content-Type": "multipart/form-data" },
    onUploadProgress,
    timeout: 60000,
  });
}

export const getMedia = () => request.get("/api/admin/media");
export const deleteMedia = (id) => request.delete(`/api/admin/media/${id}`);
