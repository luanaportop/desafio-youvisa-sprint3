// src/components/Chatbot.tsx
import React, { useState } from "react";

interface Message {
  from: "user" | "bot";
  text: string;
}

const Chatbot: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      from: "bot",
      text:
        "Olá! Sou a YOUVISA. Vamos iniciar sua solicitação de visto de turismo. " +
        "Envie seus documentos: passaporte, comprovante de residência, comprovante financeiro e formulário YOUVISA.",
    },
  ]);

  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;

    const novaMensagemUsuario: Message = { from: "user", text: input.trim() };

    // resposta simples simulada
    const respostaBot: Message = {
      from: "bot",
      text:
        "Mensagem recebida. Você também pode enviar seus documentos na área de upload ao lado. " +
        "O status será atualizado automaticamente.",
    };

    setMessages((prev) => [...prev, novaMensagemUsuario, respostaBot]);
    setInput("");
  };

  return (
    <div style={{ border: "1px solid #ccc", padding: 16, borderRadius: 8, height: "100%", display: "flex", flexDirection: "column" }}>
      <h3>Chatbot YOUVISA</h3>

      <div
        style={{
          flex: 1,
          overflowY: "auto",
          marginBottom: 8,
          border: "1px solid #eee",
          padding: 8,
          borderRadius: 4,
          background: "#fafafa",
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              marginBottom: 6,
              textAlign: msg.from === "user" ? "right" : "left",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "6px 10px",
                borderRadius: 12,
                background: msg.from === "user" ? "#d1e7ff" : "#e9ecef",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
      </div>

      <div style={{ display: "flex", gap: 8 }}>
        <input
          style={{ flex: 1 }}
          type="text"
          placeholder="Digite sua mensagem..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Enviar</button>
      </div>
    </div>
  );
};

export default Chatbot;
