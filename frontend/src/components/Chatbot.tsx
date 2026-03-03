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
      text:
        "Olá! Sou a assistente virtual YOUVISA. Posso ajudar com documentos necessários, status do processo ou dúvidas sobre o visto.",
    },
  ]);

  const [inputValue, setInputValue] = useState("");
  const [nextId, setNextId] = useState(2);
  const [isTyping, setIsTyping] = useState(false);

  // ---------------- DOCUMENTOS PADRÃO ----------------

  const listaDocumentosPadrao = (): string =>
    [
      "• Passaporte",
      "• Comprovante de residência",
      "• Comprovante financeiro",
      "• Formulário YOUVISA preenchido",
    ].join("\n");

  // ---------------- PENDÊNCIAS ----------------

  const descrevePendencias = (): string => {

    if (!statusData || !statusData.documentos) return "";

    const pendentes = statusData.documentos.filter(
      (d: any) => d.status === "PENDENTE_CORRECAO"
    );

    if (pendentes.length === 0) return "";

    return pendentes
      .map((d: any) => {
        const motivo = d.validation_reason
          ? ` — motivo: ${d.validation_reason}`
          : "";
        return `• ${d.filename}${motivo}`;
      })
      .join("\n");
  };

  // ---------------- DOCUMENTOS FALTANDO ----------------

  const descreveFaltando = (): string => {

    if (!statusData || !statusData.tipos_faltando) return "";

    const mapa: Record<string, string> = {
      passaporte: "Passaporte",
      comprovante_residencia: "Comprovante de residência",
      comprovante_financeiro: "Comprovante financeiro",
      formulario: "Formulário YOUVISA preenchido",
    };

    const nomes = statusData.tipos_faltando.map(
      (t: string) => mapa[t] ?? t
    );

    if (nomes.length === 0) return "";

    return nomes.map((n: string) => `• ${n}`).join("\n");
  };

  // ---------------- DOCUMENTOS ENVIADOS ----------------

  const listarDocumentosEnviados = (): string => {

    if (!statusData || !statusData.documentos || statusData.documentos.length === 0) {
      return "Nenhum documento foi enviado ainda.";
    }

    return statusData.documentos
      .map((d: any) => `• ${d.filename} — ${d.status}`)
      .join("\n");
  };

  // ---------------- IA GENERATIVA (SIMULADA) ----------------

  const gerarRespostaIA = () => {

    if (!statusData) {
      return "Ainda não encontrei dados do seu processo no sistema.";
    }

    const faltando = descreveFaltando();
    const pendencias = descrevePendencias();

    if (statusData.status_global === "CONCLUIDO") {
      return "Seu processo está completo. Todos os documentos foram validados com sucesso. 🎉";
    }

    if (pendencias) {
      return (
        "Identifiquei que alguns documentos precisam de correção:\n" +
        pendencias +
        "\n\nApós reenviar os documentos corrigidos, o processo continuará automaticamente."
      );
    }

    if (faltando) {
      return (
        "Seu processo ainda não está completo. Ainda precisamos dos seguintes documentos:\n" +
        faltando +
        "\n\nAssim que todos forem enviados, o sistema seguirá para validação final."
      );
    }

    return "Seu processo está em análise pela plataforma YOUVISA.";
  };

  // ---------------- INTENTS ----------------

  const buildBotResponse = (userText: string): string => {

    const text = userText.toLowerCase();

    // SAUDAÇÕES
    if (
      text.includes("oi") ||
      text.includes("olá") ||
      text.includes("ola") ||
      text.includes("bom dia") ||
      text.includes("boa tarde") ||
      text.includes("boa noite")
    ) {
      return "Olá! 😊 Posso ajudar com documentos necessários, status do processo ou dúvidas sobre o visto.";
    }

    // DOCUMENTOS NECESSÁRIOS
    if (
      text.includes("documento") ||
      text.includes("quais documentos") ||
      text.includes("o que enviar")
    ) {
      return (
        "Para solicitar o visto de turismo, você deve enviar os seguintes documentos:\n" +
        listaDocumentosPadrao() +
        "\n\nEnvie tudo em formato JPEG ou PNG."
      );
    }

    // DOCUMENTOS ENVIADOS
    if (
      text.includes("enviei") ||
      text.includes("quais enviei") ||
      text.includes("documentos enviados")
    ) {
      return listarDocumentosEnviados();
    }

    // STATUS DO PROCESSO
    if (
      text.includes("status") ||
      text.includes("processo") ||
      text.includes("andamento") ||
      text.includes("progresso")
    ) {
      return gerarRespostaIA();
    }

    // O QUE FALTA
    if (
      text.includes("o que falta") ||
      text.includes("pendencia") ||
      text.includes("pendência")
    ) {

      const faltando = descreveFaltando();
      const pendencias = descrevePendencias();

      if (pendencias) {
        return (
          "Há documentos com pendência de correção:\n" +
          pendencias
        );
      }

      if (faltando) {
        return (
          "Ainda faltam os seguintes documentos obrigatórios:\n" +
          faltando
        );
      }

      return "No momento não há pendências no seu processo.";
    }

    // FORMATOS
    if (
      text.includes("pdf") ||
      text.includes("formato")
    ) {
      return "No momento aceitamos apenas arquivos JPEG ou PNG. Caso tenha PDF, converta para imagem antes de enviar.";
    }

    // FALLBACK
    return "Não entendi completamente sua pergunta. Você pode perguntar sobre documentos necessários ou status do processo.";
  };

  // ---------------- ENVIO ----------------

  const handleSend = (e: React.FormEvent) => {

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

    const response = buildBotResponse(trimmed);

    setTimeout(() => {

      setMessages((prev) => [
        ...prev,
        {
          id: nextId + 1,
          from: "bot",
          text: response,
        },
      ]);

      setNextId((prev) => prev + 1);
      setIsTyping(false);

    }, 600);
  };

  // ---------------- UI ----------------

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