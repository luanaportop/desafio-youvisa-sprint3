// src/services/api.ts

import axios from "axios";

// -----------------------------------------------------
// 1. Instância principal do Axios
// -----------------------------------------------------
// Ajuste o baseURL se usar outra porta ou servidor.
const api = axios.create({
  baseURL: "http://localhost:8000",
});

// -----------------------------------------------------
// 2. Função: enviar documento para o backend
// -----------------------------------------------------
// IMPORTANTE: o backend FastAPI espera o campo "file"
export const uploadDocument = async (file: File) => {
  const formData = new FormData();

  // Nome do campo TEM QUE SER "file"
  formData.append("file", file);

  const response = await api.post("/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data; // retorna o documento criado no backend
};

// -----------------------------------------------------
// 3. Função: obter status global e lista de documentos
// -----------------------------------------------------
export const getStatus = async () => {
  const response = await api.get("/status");
  return response.data; // { status_global, documentos }
};

// -----------------------------------------------------
// 4. Função: health check do backend
// -----------------------------------------------------
export const checkHealth = async () => {
  const response = await api.get("/health");
  return response.data; // { status: "ok" }
};

// -----------------------------------------------------
// Exportação padrão (caso queira usar api diretamente)
// -----------------------------------------------------
export default api;
