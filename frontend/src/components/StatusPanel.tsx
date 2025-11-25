// src/components/StatusPanel.tsx
import React from "react";

interface StatusPanelProps {
  loading: boolean;
  data: any | null;
}

const StatusPanel: React.FC<StatusPanelProps> = ({ loading, data }) => {
  return (
    <div style={{ border: "1px solid #ccc", padding: 16, borderRadius: 8 }}>
      <h3>Status do Processo</h3>

      {loading && <p>Carregando status...</p>}

      {!loading && !data && <p>Nenhum dado de status disponível.</p>}

      {!loading && data && (
        <div style={{ fontSize: 14 }}>
          <p>
            <strong>Status global:</strong> {data.global_status}
          </p>

          {Array.isArray(data.documents) && data.documents.length > 0 ? (
            <ul>
              {data.documents.map((doc: any) => (
                <li key={doc.id}>
                  <strong>{doc.filename}</strong> – {doc.type} –{" "}
                  {doc.status} ({doc.validation_reason ?? "OK"})
                </li>
              ))}
            </ul>
          ) : (
            <p>Nenhum documento enviado ainda.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default StatusPanel;
