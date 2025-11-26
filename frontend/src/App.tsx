// src/App.tsx
// Componente raiz do frontend YOUVISA Sprint 2
// Aqui só organizamos layout, estilo e integração entre os componentes.

import React, { useEffect, useState } from "react";

import UploadArea from "./components/UploadArea";
import StatusPanel from "./components/StatusPanel";
import Chatbot from "./components/Chatbot";

import { checkHealth, getStatus } from "./services/api";

const App: React.FC = () => {
  // Status da API (healthcheck)
  const [apiOk, setApiOk] = useState<boolean | null>(null);

  // Dados do status global vindos do backend (/status)
  const [statusData, setStatusData] = useState<any | null>(null);

  // Flag de carregamento do status
  const [loadingStatus, setLoadingStatus] = useState(false);

  // Mensagem exibida no card "Mensagens do sistema"
  const [message, setMessage] = useState<string>("");

  // Função que consulta o endpoint /status
  const loadStatus = async () => {
    try {
      setLoadingStatus(true);
      const data = await getStatus();
      setStatusData(data);
    } catch (err) {
      console.error("Erro ao carregar status:", err);
    } finally {
      setLoadingStatus(false);
    }
  };

  // Efeito inicial: checa health e carrega status na abertura da página
  useEffect(() => {
    const init = async () => {
      try {
        const health = await checkHealth();
        setApiOk(health.status === "ok");
      } catch (err) {
        setApiOk(false);
      }

      await loadStatus();
    };
    init();
  }, []);

  // Estilo base dos "cards" principais da interface
  const cardStyle: React.CSSProperties = {
    borderRadius: 14,
    padding: 22,
    backgroundColor: "#ffffff",
    border: "1px solid #e2e7f1",
    boxShadow: "0 5px 14px rgba(15, 23, 42, 0.05)",
    marginBottom: 22,
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #eef2f7 0%, #f4f6fb 100%)",
        padding: "40px 16px 24px 16px",
        fontFamily:
          "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto",
        color: "#1f2933",
      }}
    >
      {/* Faixa superior sutil (estilo sistema oficial) */}
      <div
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          right: 0,
          height: 4,
          background:
            "linear-gradient(90deg, #2563eb 0%, #4f46e5 50%, #0ea5e9 100%)",
          zIndex: 10,
        }}
      />

      <div style={{ maxWidth: 920, margin: "0 auto" }}>
        {/* Cabeçalho da aplicação */}
        <header style={{ marginBottom: 30 }}>
          <h1
            style={{
              fontSize: 32,
              marginBottom: 6,
              letterSpacing: 0.4,
              fontWeight: 700,
              color: "#1f2d50",
            }}
          >
            YOUVISA – Sprint 2
          </h1>
          <p style={{ margin: 0, color: "#6b7280", fontSize: 15 }}>
            Portal simplificado para envio e acompanhamento de documentos do
            visto de turismo.
          </p>
        </header>

        {/* Alerta se o backend estiver offline */}
        {apiOk === false && (
          <div
            style={{
              ...cardStyle,
              backgroundColor: "#ffecec",
              borderColor: "#f5b5b5",
            }}
          >
            <strong style={{ color: "#b91c1c" }}>⚠ Backend offline</strong>
            <p style={{ marginTop: 6, fontSize: 14 }}>
              Verifique se o servidor FastAPI está ativo na porta 8000.
            </p>
          </div>
        )}

        {/* Card de upload de documentos */}
        <div style={cardStyle}>
          <UploadArea onUploaded={loadStatus} onMessage={setMessage} />
        </div>

        {/* Card de mensagens do sistema */}
        <div style={cardStyle}>
          <strong style={{ fontSize: 17 }}>Mensagens do sistema</strong>
          <p style={{ marginTop: 8, color: "#4b5563" }}>
            {message || "Nenhuma mensagem ainda."}
          </p>
        </div>

        {/* Card de status do processo */}
        <div style={cardStyle}>
          <StatusPanel statusData={statusData} loading={loadingStatus} />
        </div>

        {/* Card do chatbot */}
        <div style={cardStyle}>
          <h3 style={{ marginTop: 0, marginBottom: 10 }}>Atendimento automatizado</h3>
          {/* Passamos o statusData para o chatbot poder responder perguntas sobre o processo */}
          <Chatbot statusData={statusData} />
        </div>

        {/* Rodapé */}
        <footer
          style={{
            marginTop: 10,
            textAlign: "center",
            fontSize: 12,
            color: "#9ca3af",
          }}
        >
          YOUVISA · Protótipo acadêmico – FIAP · {new Date().getFullYear()}
        </footer>
      </div>
    </div>
  );
};

export default App;


