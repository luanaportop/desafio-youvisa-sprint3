from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

app = FastAPI(
    title="YOUVISA Sprint 2 - Backend",
    version="1.0.0",
    description="API básica para receber arquivos e expor status do processo."
)

# --------------------- CORS ---------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------- MODELOS ---------------------

class DocumentStatus(str):
    AGUARDANDO = "AGUARDANDO_VALIDACAO"
    CONCLUIDO = "CONCLUIDO"
    PENDENTE = "PENDENTE_CORRECAO"


class Document(BaseModel):
    id: str
    filename: str
    type: str              # tipo lógico (passaporte, comprovante_residencia, etc.)
    status: str
    created_at: str
    validation_reason: Optional[str] = None


# Lista de documentos simulada (memória)
documents_db: List[Document] = []


# --------------------- FUNÇÃO HÍBRIDA DE E-MAIL ---------------------

def send_email(to_email: str, subject: str, message: str):
    """
    Envia e-mail real SE variáveis de ambiente SMTP estiverem configuradas.
    Senão, simula o envio imprimindo no terminal.
    """

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    # Caso NÃO esteja configurado → SIMULAÇÃO
    if not smtp_server or not smtp_user or not smtp_pass:
        print("\n--- SIMULAÇÃO DE ENVIO DE E-MAIL ---")
        print(f"Para: {to_email}")
        print(f"Assunto: {subject}")
        print("Mensagem:")
        print(message)
        print("-------------------------------------\n")
        return {"simulated": True}

    # Envio real
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email

        with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print("E-mail REAL enviado com sucesso!")
        return {"sent": True}

    except Exception as e:
        print(f"Erro ao enviar e-mail real: {e}")
        return {"error": str(e)}


# --------------------- DETECÇÃO DE TIPO DE DOCUMENTO ---------------------

def detectar_tipo_documento(filename: str) -> str:
    """
    Decide o tipo lógico do documento com base no nome do arquivo.
    Aceita variações como 'endereco' ou 'residencia' para comprovante de residência.
    """
    name = filename.lower()

    # Passaporte
    if "passaport" in name:  # cobre 'passaporte', 'passport', etc.
        return "passaporte"

    # Comprovante de residência (endereço)
    if "comprovante" in name and (
        "residencia" in name
        or "residência" in name
        or "endereco" in name
        or "endereço" in name
    ):
        return "comprovante_residencia"

    # Comprovante financeiro
    if "financeir" in name or "renda" in name or "banc" in name:
        return "comprovante_financeiro"

    # Formulário
    if "formulario" in name or "formulário" in name:
        return "formulario"

    # Caso não bata com nada conhecido
    return "desconhecido"


# --------------------- HEALTH CHECK ---------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# --------------------- UPLOAD DE DOCUMENTO ---------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    is_image = file_extension in ["jpg", "jpeg", "png"]
    is_pdf = file_extension == "pdf"

    doc_id = str(uuid.uuid4())

    # tipo lógico do documento (passaporte, comprovante_residencia, etc.)
    doc_type = detectar_tipo_documento(file.filename)

    # ----------------- Lógica de validação simulada -----------------

    if is_image:
        status = DocumentStatus.CONCLUIDO
        reason = "Documento válido (validação básica simulada)."

        send_email(
            to_email="usuario@exemplo.com",
            subject="Documento recebido com sucesso",
            message=f"Seu documento '{file.filename}' foi validado com sucesso."
        )

    elif is_pdf:
        status = DocumentStatus.PENDENTE
        reason = "Arquivo não é uma imagem válida."

        send_email(
            to_email="usuario@exemplo.com",
            subject="Documento inválido — ação necessária",
            message=f"O documento '{file.filename}' não passou na validação. Favor reenviar em JPEG ou PNG."
        )

    else:
        status = DocumentStatus.PENDENTE
        reason = "Formato de arquivo não suportado."

        send_email(
            to_email="usuario@exemplo.com",
            subject="Documento inválido — ação necessária",
            message=f"O arquivo '{file.filename}' possui formato não suportado. Envie em JPEG ou PNG."
        )

    document = Document(
        id=doc_id,
        filename=file.filename,
        type=doc_type,
        status=status,
        created_at=datetime.utcnow().isoformat() + "Z",  # Simulação de timestamp
        validation_reason=reason
    )

    documents_db.append(document)
    return document


# --------------------- STATUS GLOBAL ---------------------

@app.get("/status")
def get_status():
    """
    Retorna:
      - status_global
      - lista de documentos
      - tipos_faltando: quais tipos obrigatórios ainda não foram enviados com sucesso

    Regras:
      - Se tiver qualquer documento PENDENTE_CORRECAO -> status_global = PENDENTE_CORRECAO
      - Senão, se faltam tipos obrigatórios          -> status_global = AGUARDANDO_VALIDACAO
      - Senão (tudo enviado e válido)                -> status_global = CONCLUIDO
    """

    # Tipos obrigatórios para o fluxo de visto de turismo
    tipos_obrigatorios = [
        "passaporte",
        "comprovante_residencia",
        "comprovante_financeiro",
        "formulario",
    ]

    # Considera como "enviado" apenas documentos CONCLUIDOS
    tipos_enviados = {
        doc.type
        for doc in documents_db
        if doc.status == DocumentStatus.CONCLUIDO
    }

    tipos_faltando = [t for t in tipos_obrigatorios if t not in tipos_enviados]

    # --- Cálculo do status_global ---

    if not documents_db:
        # nada enviado ainda
        global_status = DocumentStatus.AGUARDANDO
    else:
        # Se existe qualquer documento pendente de correção
        if any(doc.status == DocumentStatus.PENDENTE for doc in documents_db):
            global_status = DocumentStatus.PENDENTE
        else:
            # Se ainda faltam tipos obrigatórios -> aguardando
            if tipos_faltando:
                global_status = DocumentStatus.AGUARDANDO
            else:
                # Todos os obrigatórios foram enviados e estão concluídos
                global_status = DocumentStatus.CONCLUIDO

    return {
        "status_global": global_status,
        "tipos_faltando": tipos_faltando,
        "documentos": documents_db,
    }

