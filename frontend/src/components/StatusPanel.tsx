// src/components/StatusPanel.tsx
// Painel de status YOUVISA – mostra status, documentos enviados e progresso.

import React from "react";

interface StatusPanelProps {
  statusData: any | null;
  loading: boolean;
}

const StatusPanel: React.FC<StatusPanelProps> = ({ statusData, loading }) => {
  if (loading && !statusData) {
    return (
      <div
        style={{
          border: "1px solid #e5e7eb",
          borderRadius: 12,
          padding: 16,
          backgroundColor: "#f9fafb",
          marginTop: 16,
        }}
      >
        <h3>Status do Processo</h3>
        <p>Carregando status...</p>
      </div>
    );
  }

  const globalStatus: string | null = statusData?.status_global ?? null;
  const documentos: any[] = statusData?.documentos ?? [];
  const tiposFaltando: string[] = statusData?.tipos_faltando ?? [];

  const mapaTipos: Record<string, string> = {
    passaporte: "Passaporte",
    comprovante_residencia: "Comprovante de residência",
    comprovante_financeiro: "Comprovante financeiro",
    formulario: "Formulário YOUVISA preenchido",
  };

  // ----------- STATUS TEXT -----------

  let statusColor = "#4b5563";
  let statusText = "Status ainda não disponível.";

  if (globalStatus === "CONCLUIDO") {
    statusColor = "#16a34a";
    statusText = "Todos os documentos foram validados com sucesso.";
  } else if (globalStatus === "PENDENTE_CORRECAO") {
    statusColor = "#dc2626";
    statusText = "Alguns documentos precisam de correção.";
  } else if (globalStatus === "AGUARDANDO_VALIDACAO") {
    statusColor = "#ea580c";

    if (documentos.length === 0) {
      statusText =
        "Nenhum documento enviado ainda. Envie seus documentos para iniciar a análise.";
    } else if (tiposFaltando.length > 0) {
      statusText =
        "Seu processo está em andamento. Alguns documentos obrigatórios ainda não foram enviados.";
    } else {
      statusText =
        "Seu processo está em fase de validação. Aguarde a atualização do status.";
    }
  }

  // ----------- PROGRESSO -----------

  const totalObrigatorios = 4;
  const enviados = totalObrigatorios - tiposFaltando.length;
  const progresso = Math.round((enviados / totalObrigatorios) * 100);

  // ----------- DOCUMENTOS FALTANDO -----------

  const faltandoHumanizado =
    tiposFaltando.length > 0
      ? tiposFaltando.map((t) => mapaTipos[t] ?? t)
      : [];

  return (
    <div
      style={{
        border: "1px solid #e5e7eb",
        borderRadius: 12,
        padding: 16,
        backgroundColor: "#f9fafb",
        marginTop: 16,
      }}
    >
      <h3>Status do Processo</h3>

      {/* Barra de progresso */}
      <div style={{ marginBottom: 12 }}>
        <strong>Progresso do envio de documentos</strong>

        <div
          style={{
            width: "100%",
            background: "#e5e7eb",
            borderRadius: 8,
            marginTop: 6,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: `${progresso}%`,
              background: "#2563eb",
              color: "white",
              textAlign: "center",
              padding: "4px 0",
              fontSize: 12,
            }}
          >
            {progresso}%
          </div>
        </div>
      </div>

      {/* Status global */}
      <p style={{ marginBottom: 4 }}>
        <strong>Status global: </strong>
        <span style={{ color: statusColor }}>{statusText}</span>
      </p>

      {/* Documentos faltando */}
      {faltandoHumanizado.length > 0 && (
        <div style={{ marginTop: 8, marginBottom: 4 }}>
          <strong>Documentos obrigatórios ainda não enviados:</strong>
          <ul style={{ marginTop: 4 }}>
            {faltandoHumanizado.map((nome) => (
              <li key={nome}>{nome}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Documentos enviados */}
      <div style={{ marginTop: 8 }}>
        <strong>Documentos enviados:</strong>

        {documentos.length === 0 ? (
          <p style={{ marginTop: 4 }}>Nenhum documento enviado ainda.</p>
        ) : (
          <ul style={{ marginTop: 4 }}>
            {documentos.map((doc) => (
              <li key={doc.id}>
                {doc.filename}{" "}
                {doc.status === "CONCLUIDO" ? (
                  <span style={{ color: "green" }}>✔</span>
                ) : (
                  <span style={{ color: "red" }}>⚠</span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default StatusPanel;