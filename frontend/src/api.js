import axios from "axios";
const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || "http://localhost:8800" });
export const uploadFile = file => {
  const f = new FormData(); f.append("file", file); return api.post("/docs/upload", f);
};
export const getPrompts = () => api.get("/prompts");
export const analyze = (fileId,promptId) => api.post("/analysis", { file_id: fileId, prompt_id: promptId });
