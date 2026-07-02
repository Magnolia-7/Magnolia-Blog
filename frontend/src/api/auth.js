import request from "./request";

export function login(data) {
  return request.post("/api/admin/login", data);
}