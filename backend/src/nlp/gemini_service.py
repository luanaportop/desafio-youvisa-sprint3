import os
from google import genai
from dotenv import load_dotenv

# Garante a leitura do .env mesmo em subpastas
load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Configuração do Cliente
api_key = os.environ.get("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

# --- MOCK DA FUNÇÃO DE LOG (Governança) ---
def log_ai_interaction(pergunta: str, resposta: str):
    """Simula o registro de auditoria exigido pela governança"""
    print(f"\n[AUDITORIA IA] Pergunta: {pergunta[:30]}... | Resposta: {resposta[:30]}...")

SYSTEM_PROMPT = """
Você é o assistente da plataforma YOUVISA.
Responda sempre em português do Brasil de forma cordial.

Regras de Governança:
- Use apenas o contexto fornecido.
- Não invente status ou documentos.
- Caso o usuário forneça senhas ou CPFs, oriente-o a não compartilhar dados sensíveis no chat.
"""

def extrair_status_do_contexto(contexto: str) -> str:
    try:
        for linha in contexto.split('\n'):
            if "Status global" in linha:
                return linha.split(':')[-1].strip()
    except Exception:
        pass
    return "em processamento"

def gerar_resposta(pergunta: str, contexto: str) -> str:
    try:
        # Verificação de segurança para API Key
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no ambiente.")

        prompt = f"{SYSTEM_PROMPT}\n\nContexto: {contexto}\n\nPergunta: {pergunta}"

        # Ajustado para modelo estável (2.0 Flash)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        ai_response = response.text
        
        # Agora a função existe e não causará erro
        log_ai_interaction(pergunta, ai_response)

        return ai_response

    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        status_atual = extrair_status_do_contexto(contexto)
        
        return (
            f"Desculpe, tive um problema técnico. "
            f"Consultando o sistema, seu status é: **{status_atual}**. "
            f"Tente novamente em instantes."
        )
