// src/App.tsx
import React, { useEffect, useState } from "react";
import Chatbot from "./components/Chatbot";
import UploadArea from "./components/UploadArea";
import StatusPanel from "./components/StatusPanel";
import { checkHealth, getStatus } from "./services/api";

const App: React.FC = () => {
  const [apiOk, setApiOk] = useState<boolean | null>(null);
  const [statusData, setStatusData] = useState<any | null>(null);
  const [loadingStatus, setLoadingStatus] = useState(false);

  const loadStatus = async () => {
    try {
      setLoadingStatus(true);
      const data = await getStatus();
      setStatusData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    // checa saúde da API e carrega status quando abrir
    const init = async () => {
      const ok = await checkHealth();
      setApiOk(ok);
      if (ok) {
        await loadStatus();
      }
    };
    init();
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "system-ui, sans-serif" }}>
      <h1>YOUVISA – Sprint 2</h1>
      <p style={{ marginBottom: 16 }}>
        Plataforma simulada de atendimento para solicitação de visto de turismo.
      </p>

      {apiOk === false && (
        <p style={{ color: "red" }}>
          ⚠ Backend indisponível. Verifique se o servidor FastAPI está rodando
          em <code>http://127.0.0.1:8000</code>.
        </p>
      )}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1.2fr 1fr",
          gap: 16,
          alignItems: "flex-start",
        }}
      >
        <Chatbot />

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <UploadArea
            onUploaded={loadStatus}
            onMessage={(msg) => alert(msg)}
          />
          <StatusPanel loading={loadingStatus} data={statusData} />
        </div>
      </div>
    </div>
  );
};

export default App;
