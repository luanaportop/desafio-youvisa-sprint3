// src/components/UploadArea.tsx
import React, { useState } from "react";
import { uploadDocument } from "../services/api";

interface UploadAreaProps {
  onUploaded: () => void; // para recarregar o status depois do upload
  onMessage: (msg: string) => void;
}

const UploadArea: React.FC<UploadAreaProps> = ({ onUploaded, onMessage }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      onMessage("Selecione um arquivo antes de enviar.");
      return;
    }

    try {
      setLoading(true);
      const result = await uploadDocument(file);
      onMessage(`Documento enviado: status = ${result.status}`);
      onUploaded();
      setFile(null);
    } catch (err: any) {
      onMessage(`Erro ao enviar documento: ${err.message ?? err}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: 16, borderRadius: 8 }}>
      <h3>Upload de Documentos</h3>
      <input
        type="file"
        onChange={(e) => {
          const f = e.target.files?.[0] ?? null;
          setFile(f);
        }}
      />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Enviando..." : "Enviar documento"}
      </button>
    </div>
  );
};

export default UploadArea;
