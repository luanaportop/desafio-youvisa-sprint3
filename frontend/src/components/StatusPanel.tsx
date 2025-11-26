// src/components/StatusPanel.tsx
// Painel de status YOUVISA – lê status_global, documentos e tipos_faltando
// e mostra mensagens coerentes com o backend.

import React from "react";

interface StatusPanelProps {
  statusData: any | null;
  loading: boolean;
}

const StatusPanel: React.FC<StatusPanelProps> = ({ statusData, loading }) => {
  // Se ainda não carregou nada
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

  // Mapa dos tipos para texto amigável (igual ao do chatbot)
  const mapaTipos: Record<string, string> = {
    passaporte: "Passaporte",
    comprovante_residencia: "Comprovante de residência",
    comprovante_financeiro: "Comprovante financeiro",
    formulario: "Formulário YOUVISA preenchido",
  };

  // ------------- Texto principal e cores -------------

  let statusColor = "#4b5563"; // cinza padrão
  let statusText = "Status ainda não disponível.";

  if (globalStatus === "CONCLUIDO") {
    statusColor = "#16a34a"; // verde
    statusText = "Todos os documentos foram validados com sucesso.";
  } else if (globalStatus === "PENDENTE_CORRECAO") {
    statusColor = "#dc2626"; // vermelho
    statusText = "Alguns documentos precisam de correção.";
  } else if (globalStatus === "AGUARDANDO_VALIDACAO") {
    statusColor = "#ea580c"; // laranja

    if (documentos.length === 0) {
      // Nenhum documento ainda
      statusText =
        "Nenhum documento enviado ainda. Envie seus documentos para iniciar a análise.";
    } else if (tiposFaltando.length > 0) {
      // Já temos alguns documentos, mas ainda faltam obrigatórios
      statusText =
        "Seu processo está em andamento. Alguns documentos obrigatórios ainda não foram enviados.";
    } else {
      // Situação rara, mas só pra não deixar sem frase
      statusText =
        "Seu processo está em fase de recebimento e validação. Aguarde a atualização do status.";
    }
  }

  // ------------- Lista de documentos faltando (opcional) -------------

  const faltandoHumanizado =
    tiposFaltando.length > 0
      ? tiposFaltando
          .map((t) => mapaTipos[t] ?? t)
          .filter(Boolean)
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

      {/* Linha do status global */}
      <p style={{ marginBottom: 4 }}>
        <strong>Status global: </strong>
        <span style={{ color: statusColor }}>{statusText}</span>
      </p>

      {/* Documentos faltando (se houver) */}
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

      {/* Lista dos documentos enviados */}
      <div style={{ marginTop: 8 }}>
        <strong>Documentos enviados:</strong>
        {documentos.length === 0 ? (
          <p style={{ marginTop: 4 }}>Nenhum documento enviado ainda.</p>
        ) : (
          <ul style={{ marginTop: 4 }}>
            {documentos.map((doc) => (
              <li key={doc.id}>
                {doc.filename} — <em>{doc.status}</em>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default StatusPanel;



