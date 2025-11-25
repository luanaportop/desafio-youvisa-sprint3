// src/services/api.ts
const API_BASE_URL = "http://127.0.0.1:8000";

export async function checkHealth(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    return res.ok;
  } catch {
    return false;
  }
}

export async function uploadDocument(file: File): Promise<any> {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    throw new Error("Falha ao enviar documento");
  }

  return res.json();
}

export async function getStatus(): Promise<any> {
  const res = await fetch(`${API_BASE_URL}/status`);

  if (!res.ok) {
    throw new Error("Falha ao consultar status");
  }

  return res.json();
}
