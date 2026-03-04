// src/components/UploadArea.tsx
// Responsável apenas pela interface e fluxo de upload de arquivos.

import React, { useState } from "react";
import toast from "react-hot-toast";
import { uploadDocument } from "../services/api";

const MIN_FILE_SIZE_BYTES = 10 * 1024;

interface UploadAreaProps {
  onUploaded: () => void;       // Chamado após upload bem-sucedido para atualizar o status global
  onMessage: (msg: string) => void; // Atualiza a mensagem exibida no card "Mensagens do sistema"
}

const UploadArea: React.FC<UploadAreaProps> = ({ onUploaded, onMessage }) => {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  // Estilo base do botão de envio
  const buttonBase: React.CSSProperties = {
    backgroundColor: "#2563eb",
    color: "white",
    padding: "7px 18px",
    borderRadius: 999,
    border: "none",
    cursor: "pointer",
    fontSize: 14,
    fontWeight: 600,
    transition: "background 0.2s, transform 0.1s",
  };

  // Fluxo de upload → chama o backend via serviço uploadDocument
  const handleUpload = async () => {
    if (!file) {
      onMessage("Selecione um arquivo antes de enviar.");
      return;
    }

    if (file.size < MIN_FILE_SIZE_BYTES) {
      toast.error(
        `Arquivo muito pequeno (${(file.size / 1024).toFixed(1)} KB). Mínimo: ${MIN_FILE_SIZE_BYTES / 1024} KB.`
      );
      return;
    }

    try {
      setLoading(true);

      const result = await uploadDocument(file);

      // Mostra o status retornado pelo backend
      onMessage(`Documento enviado. Status = ${result.status}`);

      // Atualiza o painel de status global
      onUploaded();

      // Limpa o input
      setFile(null);
    } catch (err: any) {
      onMessage(`Erro ao enviar: ${err.message ?? err}`);
      if (err.response?.data?.detail) {
        onMessage(err.response.data.detail)
      } else {
        onMessage("Erro ao enviar documento.")
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3 style={{ marginTop: 0, marginBottom: 4 }}>Upload de Documentos</h3>
      <p style={{ margin: "0 0 14px 0", color: "#6b7280", fontSize: 13 }}>
        <em>Tipos aceitos: JPEG ou PNG.</em>
      </p>

      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
          flexWrap: "wrap",
        }}
      >
        {/* Input de arquivo com filtro de tipos aceitos */}
        <input
          type="file"
          accept="image/jpeg, image/png"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
          style={{
            fontSize: 13,
            padding: 4,
          }}
        />

        {/* Botão de envio */}
        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            ...buttonBase,
            opacity: loading ? 0.75 : 1,
            backgroundColor: loading ? "#1e40af" : "#2563eb",
          }}
          onMouseDown={(e) => {
            // Efeito de "click" levemente pressionado
            (e.currentTarget as HTMLButtonElement).style.transform =
              "scale(0.98)";
          }}
          onMouseUp={(e) => {
            (e.currentTarget as HTMLButtonElement).style.transform = "scale(1)";
          }}
          onMouseLeave={(e) => {
            (e.currentTarget as HTMLButtonElement).style.transform = "scale(1)";
          }}
        >
          {loading ? "Enviando..." : "Enviar documento"}
        </button>
      </div>
    </div>
  );
};

export default UploadArea;

