fimport os
from google import genai
from dotenv import load_dotenv # 1. Importar a biblioteca
from .ai_governance import log_ai_interaction

load_dotenv() 

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


# SYSTEM_PROMPT com Regras de Governança
SYSTEM_PROMPT = """
Você é o assistente da plataforma YOUVISA.

Responda sempre em português do Brasil.
Seja claro, objetivo e cordial.

Regras:
- Use apenas as informações fornecidas no contexto do sistema.
- Não invente documentos enviados ou status.
- Se faltarem documentos, informe quais faltam de acordo com o contexto.
- Se todos os documentos estiverem concluídos, diga que o processo está em análise.
- Não prometa aprovação de visto ou prazos finais (decisões são exclusivas do consulado).
- Caso a pergunta esteja fora do escopo, responda que só ajuda com documentos e status do processo YOUVISA.

# --- GOVERNANÇA E PRIVACIDADE (LGPD) ---
- Caso o usuário forneça dados sensíveis como senhas ou CPFs, oriente-o educadamente a não compartilhar essas informações no chat por segurança.
"""

def extrair_status_do_contexto(contexto: str) -> str:
    """Função auxiliar para o fallback buscar o status no texto do contexto"""
    try:
        # Busca a linha que contém o status global no bloco de texto enviado
        for linha in contexto.split('\n'):
            if "Status global" in linha:
                return linha.split(':')[-1].strip()
    except Exception:
        pass
    return "em processamento"

def gerar_resposta(pergunta: str, contexto: str) -> str:
    """
    Gera resposta via Gemini com tratamento de erro (Fallback) 
    e log de governança.
    """
    # --- INÍCIO DA MELHORIA (Bloco Try para Robustez) ---
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
        
        ai_response = response.text
        
        # Registro da interação para auditoria
        log_ai_interaction(pergunta, ai_response)

        return ai_response

    # --- TRATAMENTO DE ERRO (Fallback de Segurança) ---
    except Exception as e:
        # Log interno do erro para o desenvolvedor
        print(f"Erro na IA: {e}")
        
        # Resposta amigável de fallback baseada nos dados reais do sistema
        status_atual = extrair_status_do_contexto(contexto)
        
        return (
            f"Desculpe, tive um problema técnico para gerar uma resposta personalizada agora. "
            f"Mas consultando o sistema, vi que seu processo está com o status: **{status_atual}**. "
            f"Por favor, tente perguntar novamente em alguns instantes."
        )
