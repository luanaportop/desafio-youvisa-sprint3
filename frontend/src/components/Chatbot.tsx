import React, { useState } from "react";

interface ChatMessage {
  id: number;
  from: "bot" | "user";
  text: string;
}

interface ChatbotProps {
  statusData: any | null;
}

const Chatbot: React.FC<ChatbotProps> = ({ statusData }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: 1,
      from: "bot",
      text: "Olá! Sou a assistente virtual YOUVISA. Posso ajudar com documentos necessários, status do processo ou dúvidas sobre o visto.",
    },
  ]);

  const [inputValue, setInputValue] = useState("");
  const [nextId, setNextId] = useState(2);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();

    const trimmed = inputValue.trim();
    if (!trimmed) return;

    const userMessage: ChatMessage = {
      id: nextId,
      from: "user",
      text: trimmed,
    };

    setMessages((prev) => [...prev, userMessage]);
    setNextId((prev) => prev + 1);
    setInputValue("");
    setIsTyping(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          pergunta: trimmed,
          statusData: statusData,
        }),
      });

      const data = await response.json();

      const botMessage: ChatMessage = {
        id: nextId + 1,
        from: "bot",
        text:
          data.resposta ||
          "Não consegui responder agora. Tente novamente em instantes.",
      };

      setMessages((prev) => [...prev, botMessage]);
      setNextId((prev) => prev + 1);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: nextId + 1,
        from: "bot",
        text: "Erro ao conectar com o assistente inteligente. Verifique se o backend está rodando.",
      };

      setMessages((prev) => [...prev, errorMessage]);
      setNextId((prev) => prev + 1);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div style={{ border: "1px solid #e5e7eb", padding: 14, borderRadius: 12 }}>
      <h4>Chatbot YOUVISA</h4>

      <div style={{ maxHeight: 250, overflowY: "auto", marginBottom: 10 }}>
        {messages.map((msg) => (
          <div key={msg.id} style={{ marginBottom: 8 }}>
            <strong>{msg.from === "bot" ? "YOUVISA" : "Você"}:</strong>
            <div style={{ whiteSpace: "pre-line" }}>{msg.text}</div>
          </div>
        ))}

        {isTyping && <div>YOUVISA está digitando...</div>}
      </div>

      <form onSubmit={handleSend} style={{ display: "flex", gap: 8 }}>
        <input
          type="text"
          placeholder="Digite sua mensagem..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          style={{ flex: 1, padding: 8 }}
        />

        <button type="submit">Enviar</button>
      </form>
    </div>
  );
};

export default Chatbot;