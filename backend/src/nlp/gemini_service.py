from google import genai

client = genai.Client()

SYSTEM_PROMPT = """ ... seu prompt atual ... """

def extrair_status_do_contexto(contexto: str) -> str:
    """Função auxiliar para o fallback buscar o status no texto do contexto"""
    try:
        # Busca a linha que contém o status global no bloco de texto enviado
        for linha in contexto.split('\n'):
            if "Status global" in linha:
                return linha.split(':')[-1].strip()
    except:
        pass
    return "em processamento"

def gerar_resposta(pergunta: str, contexto: str) -> str:
    # --- INÍCIO DA MELHORIA (Bloco Try) ---
    try:
        prompt = f"""
        {SYSTEM_PROMPT}

        Contexto do sistema:
        {contexto}

        Pergunta do usuário:
        {pergunta}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    # --- TRATAMENTO DE ERRO (Fallback) ---
    except Exception as e:
        print(f"Erro na IA: {e}")
        status_atual = extrair_status_do_contexto(contexto)
        return (
            f"Desculpe, tive um problema técnico para gerar uma resposta personalizada agora. "
            f"Mas consultando o sistema, vi que seu processo está com o status: **{status_atual}**. "
            f"Por favor, tente perguntar novamente em alguns instantes."
        )
