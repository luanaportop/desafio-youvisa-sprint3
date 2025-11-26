// src/components/Chatbot.tsx
// Chatbot YOUVISA SmartChat 2.1 – usa tipos_faltando do backend
// - NÃO altera a lógica do backend
// - Só melhora as respostas para "o que falta?" e "qual documento devo enviar?"

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
        "Olá! Sou a assistente virtual YOUVISA. " +
        "Estou aqui para te ajudar com o envio dos documentos e o status do seu visto de turismo.",
    },
  ]);

  const [inputValue, setInputValue] = useState("");
  const [nextId, setNextId] = useState(2);
  const [isTyping, setIsTyping] = useState(false);

  // ----------------- AUXILIARES -----------------

  const listaDocumentosPadrao = (): string =>
    [
      "• Passaporte",
      "• Comprovante de residência",
      "• Comprovante financeiro",
      "• Formulário YOUVISA preenchido",
    ].join("\n");

  const descrevePendencias = (): string => {
    if (!statusData || !statusData.documentos) return "";
    const pendentes = (statusData.documentos as any[]).filter(
      (d) => d.status === "PENDENTE_CORRECAO"
    );
    if (pendentes.length === 0) return "";
    const linhas = pendentes.map((d) => {
      const motivo = d.validation_reason
        ? ` — motivo: ${d.validation_reason}`
        : "";
      return `• ${d.filename}${motivo}`;
    });
    return linhas.join("\n");
  };

  // traduz tipos_faltando em texto legível
  const descreveFaltandoObrigatorios = (): string => {
    if (!statusData || !Array.isArray(statusData.tipos_faltando)) return "";

    const mapa: Record<string, string> = {
      passaporte: "Passaporte",
      comprovante_residencia: "Comprovante de residência",
      comprovante_financeiro: "Comprovante financeiro",
      formulario: "Formulário YOUVISA preenchido",
    };

    const nomes = (statusData.tipos_faltando as string[])
      .map((t) => mapa[t] ?? t)
      .filter(Boolean);

    if (!nomes.length) return "";

    return nomes.map((n) => `• ${n}`).join("\n");
  };

  // ----------------- INTENTS -----------------

  const buildBotResponse = (userText: string): string => {
    const text = userText.toLowerCase();
    const pendenciasTexto = descrevePendencias();
    const faltandoTexto = descreveFaltandoObrigatorios();

    // 1) Saudações
    if (
      text.includes("oi") ||
      text.includes("olá") ||
      text.includes("ola") ||
      text.includes("bom dia") ||
      text.includes("boa tarde") ||
      text.includes("boa noite")
    ) {
      return (
        "Olá! 😊 Sou a assistente virtual YOUVISA. " +
        "Posso te explicar quais documentos enviar, falar sobre o status do seu processo " +
        "ou tirar dúvidas sobre o visto de turismo."
      );
    }

    // 2) Pergunta sobre quais documentos enviar
    if (
      text.includes("documento") ||
      text.includes("documentos") ||
      text.includes("preciso enviar") ||
      text.includes("quais documentos") ||
      text.includes("qual documento") ||
      text.includes("o que enviar") ||
      text.includes("o que devo enviar") ||
      text.includes("não sei o que enviar") ||
      text.includes("nao sei o que enviar")
    ) {
      // Se houver pendências de correção
      if (pendenciasTexto) {
        return (
          "Você já enviou alguns documentos, mas ainda existem pendências que precisam de correção:\n" +
          pendenciasTexto +
          "\n\nDe forma geral, para o visto de turismo, são necessários:\n" +
          listaDocumentosPadrao() +
          "\n\nEnvie ou reenvie tudo em formato JPEG ou PNG."
        );
      }

      // Se ainda faltam documentos obrigatórios (mas sem pendência de formato)
      if (faltandoTexto) {
        return (
          "Você já enviou parte da documentação, mas ainda faltam os seguintes documentos obrigatórios:\n" +
          faltandoTexto +
          "\n\nPara o visto de turismo, no total, são necessários:\n" +
          listaDocumentosPadrao() +
          "\n\nVocê pode anexar os arquivos restantes em formato JPEG ou PNG na área de upload acima."
        );
      }

      // Nenhuma pendência e nada faltando → lista padrão
      return (
        "Para o visto de turismo, você deve enviar os seguintes documentos:\n" +
        listaDocumentosPadrao() +
        "\n\nLembre-se de anexar tudo em formato JPEG ou PNG na área de upload acima."
      );
    }

    // 3) Dúvida sobre formatos / PDF
    if (
      text.includes("pdf") ||
      text.includes("formato") ||
      text.includes("tipo de arquivo")
    ) {
      return (
        "No momento, o sistema YOUVISA aceita apenas imagens nos formatos JPEG ou PNG. " +
        "Se você tiver um documento em PDF, é só convertê-lo para imagem antes de enviar."
      );
    }

    // 4) Pergunta sobre status ou andamento do processo
    if (
      text.includes("status") ||
      text.includes("processo") ||
      text.includes("como está") ||
      text.includes("andamento") ||
      text.includes("progresso")
    ) {
      if (!statusData) {
        return (
          "Ainda não tenho informações de status carregadas. " +
          "Assim que você enviar documentos, o painel de status acima será atualizado automaticamente."
        );
      }

      const globalStatus = statusData.status_global;

      if (globalStatus === "CONCLUIDO") {
        return (
          "Boa notícia! 🎉 Todos os seus documentos foram validados com sucesso. " +
          "Seu processo está pronto para seguir para a próxima etapa."
        );
      }

      if (globalStatus === "PENDENTE_CORRECAO") {
        return (
          "Encontrei pendências no seu processo. Alguns documentos precisam de correção:\n" +
          (pendenciasTexto ? "\n" + pendenciasTexto : "") +
          "\n\nVocê pode reenviar os documentos corrigidos na área de upload acima."
        );
      }

      // AGUARDANDO validação / envio
      if (
        globalStatus === "AGUARDANDO_VALIDACAO" ||
        globalStatus === "AGUARDANDO"
      ) {
        if (faltandoTexto) {
          return (
            "Seu processo ainda está em andamento. Até o momento, foram recebidos alguns documentos, " +
            "mas ainda faltam os seguintes itens obrigatórios:\n" +
            faltandoTexto +
            "\n\nEnvie os documentos restantes em formato JPEG ou PNG para avançar para a próxima etapa."
          );
        }

        return (
          "Seu processo está em fase de recebimento e validação. " +
          "Se você enviou documentos há poucos instantes, aguarde alguns segundos e o status será atualizado."
        );
      }

      // fallback inesperado
      return (
        "Estou com dificuldade para interpretar o status atual do sistema. " +
        "Tente atualizar a página ou consultar o painel de status acima."
      );
    }

    // 5) Pergunta direta sobre pendências / o que falta
    if (
      text.includes("pendência") ||
      text.includes("pendencia") ||
      text.includes("o que falta") ||
      text.includes("tem algo faltando") ||
      text.includes("falta algum documento")
    ) {
      // Se houver pendência de arquivo inválido
      if (pendenciasTexto) {
        return (
          "Há documentos com pendência de correção no seu processo:\n" +
          pendenciasTexto +
          "\n\nVocê pode reenviar as versões corrigidas na área de upload acima."
        );
      }

      // Se não há pendências de formato, mas faltam obrigatórios
      if (faltandoTexto) {
        return (
          "Ainda faltam alguns documentos obrigatórios para concluir seu processo:\n" +
          faltandoTexto +
          "\n\nQuando todos forem enviados em JPEG ou PNG, o status mudará para concluído."
        );
      }

      // Nada faltando + nada pendente
      if (statusData && statusData.status_global === "CONCLUIDO") {
        return "No momento, não há pendências. Todos os documentos foram validados com sucesso. 🎉";
      }

      return (
        "Não encontrei pendências claras, mas o painel de status acima traz o detalhamento do processo em tempo real."
      );
    }

    // 6) Quando o usuário fala que enviou alguma coisa
    if (
      text.includes("enviei") ||
      text.includes("acabei de enviar") ||
      text.includes("mandei") ||
      text.includes("já mandei") ||
      text.includes("ja mandei") ||
      text.includes("já enviei") ||
      text.includes("ja enviei")
    ) {
      return (
        "Perfeito, já registrei o envio do seu documento. " +
        "O sistema YOUVISA fará a validação automaticamente e o status será atualizado no painel acima."
      );
    }

    // 7) Dúvidas genéricas
    if (
      text.includes("ajuda") ||
      text.includes("não sei") ||
      text.includes("nao sei") ||
      text.includes("dúvida") ||
      text.includes("duvida")
    ) {
      return (
        "Estou aqui para te ajudar! 💙 " +
        "Você pode me perguntar sobre: documentos necessários, formatos aceitos ou status do seu processo."
      );
    }

    // 8) Fallback
    return (
      "Entendi sua mensagem, mas talvez eu precise de um pouco mais de contexto. " +
      "Você pode perguntar, por exemplo: 'quais documentos preciso enviar?', " +
      "'qual é o status do meu processo?' ou 'posso enviar PDF?'."
    );
  };

  // ----------------- ENVIO -----------------

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

    const responseText = buildBotResponse(trimmed);

    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          id: nextId + 1,
          from: "bot",
          text: responseText,
        },
      ]);
      setNextId((prev) => prev + 1);
      setIsTyping(false);
    }, 600);
  };

  // ----------------- ESTILOS -----------------

  const containerStyle: React.CSSProperties = {
    borderRadius: 16,
    border: "1px solid #e5e7eb",
    background:
      "linear-gradient(135deg, rgba(255,255,255,0.98), rgba(248,250,252,0.98))",
    padding: 14,
    boxShadow: "0 8px 18px rgba(15,23,42,0.08)",
  };

  const messagesAreaStyle: React.CSSProperties = {
    maxHeight: 240,
    overflowY: "auto",
    padding: "10px 6px",
    backgroundColor: "#f3f4f6",
    borderRadius: 12,
    border: "1px solid #e5e7eb",
    marginBottom: 10,
  };

  const inputWrapperStyle: React.CSSProperties = {
    display: "flex",
    gap: 8,
    marginTop: 6,
  };

  const inputStyle: React.CSSProperties = {
    flex: 1,
    borderRadius: 999,
    border: "1px solid #d1d5db",
    padding: "7px 12px",
    fontSize: 13,
    outline: "none",
    backgroundColor: "#ffffff",
  };

  const buttonStyle: React.CSSProperties = {
    borderRadius: 999,
    background: "linear-gradient(135deg, #2563eb, #1d4ed8)",
    color: "#fff",
    border: "none",
    padding: "7px 16px",
    fontSize: 13,
    fontWeight: 600,
    cursor: "pointer",
    boxShadow: "0 4px 10px rgba(37,99,235,0.35)",
  };

  return (
    <div style={containerStyle}>
      <h4 style={{ marginTop: 0, marginBottom: 10 }}>Chatbot YOUVISA</h4>

      <div style={messagesAreaStyle}>
        {messages.map((msg) => {
          const isBot = msg.from === "bot";

          const bubbleStyle: React.CSSProperties = isBot
            ? {
                maxWidth: "80%",
                padding: "8px 12px",
                borderRadius: 14,
                fontSize: 13,
                lineHeight: 1.5,
                background: "linear-gradient(135deg, #eef2ff, #e5e7eb)",
                color: "#111827",
                whiteSpace: "pre-line",
                boxShadow: "0 3px 8px rgba(15,23,42,0.08)",
              }
            : {
                maxWidth: "80%",
                padding: "8px 12px",
                borderRadius: 14,
                fontSize: 13,
                lineHeight: 1.5,
                backgroundColor: "#dbeafe",
                color: "#111827",
                whiteSpace: "pre-line",
                boxShadow: "0 3px 8px rgba(37,99,235,0.18)",
              };

          return (
            <div
              key={msg.id}
              style={{
                display: "flex",
                justifyContent: isBot ? "flex-start" : "flex-end",
                marginBottom: 8,
              }}
            >
              <div style={bubbleStyle}>
                {isBot && (
                  <div
                    style={{
                      fontSize: 11,
                      fontWeight: 600,
                      color: "#4b5563",
                      marginBottom: 3,
                    }}
                  >
                    YOUVISA
                  </div>
                )}
                {!isBot && (
                  <div
                    style={{
                      fontSize: 11,
                      fontWeight: 600,
                      color: "#1d4ed8",
                      marginBottom: 3,
                      textAlign: "right",
                    }}
                  >
                    Você
                  </div>
                )}
                <div>{msg.text}</div>
              </div>
            </div>
          );
        })}

        {isTyping && (
          <div
            style={{
              display: "flex",
              justifyContent: "flex-start",
              marginTop: 4,
            }}
          >
            <div
              style={{
                padding: "4px 10px",
                borderRadius: 999,
                backgroundColor: "#e5e7eb",
                fontSize: 11,
                color: "#6b7280",
                fontStyle: "italic",
              }}
            >
              YOUVISA está digitando...
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSend}>
        <div style={inputWrapperStyle}>
          <input
            type="text"
            placeholder="Digite sua mensagem..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            style={inputStyle}
          />
          <button type="submit" style={buttonStyle}>
            Enviar
          </button>
        </div>
      </form>
    </div>
  );
};

export default Chatbot;


    