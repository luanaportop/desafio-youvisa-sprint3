from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import os
import smtplib
from dotenv import load_dotenv

# Carrega variáveis de .env (pasta backend ou backend/src)
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
from email.mime.text import MIMEText
from datetime import datetime

from events.event_bus import publish, subscribe
from notifications.status_notification import handle_status_change

from database.init_db import init_db
from database.db import get_connection
from document_validation import validate_image


app = FastAPI(
    title="YOUVISA Sprint 3 - Backend",
    version="1.0.0",
    description="API para upload de documentos e acompanhamento do processo de visto."
)

# inicializa banco
init_db()

# Diretório onde os arquivos enviados são salvos (relativo ao diretório deste arquivo)
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")


def ensure_uploads_dir():
    os.makedirs(UPLOADS_DIR, exist_ok=True)


ensure_uploads_dir()


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
    type: str
    status: str
    created_at: str
    validation_reason: Optional[str] = None


# --------------------- EMAIL ---------------------

def send_email(to_email: str, subject: str, message: str):

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")

    # Simulação caso não exista SMTP
    if not smtp_server or not smtp_user or not smtp_pass:
        print("\n--- SIMULAÇÃO DE ENVIO DE E-MAIL ---")
        print(f"Para: {to_email}")
        print(f"Assunto: {subject}")
        print("Mensagem:")
        print(message)
        print("-------------------------------------\n")
        return

    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = to_email

        with smtplib.SMTP_SSL(smtp_server, int(smtp_port)) as server:
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


# --------------------- DETECÇÃO DE DOCUMENTO ---------------------

def detectar_tipo_documento(filename: str) -> str:

    name = filename.lower()

    # Passaporte
    if "passaporte" in name or "passport" in name:
        return "passaporte"

    # Comprovante de residência
    if "residencia" in name or "residência" in name or "endereco" in name or "endereço" in name:
        return "comprovante_residencia"

    # Comprovante financeiro
    if "financeiro" in name or "renda" in name or "banc" in name:
        return "comprovante_financeiro"

    # Formulário
    if "formulario" in name:
        return "formulario"

    return "desconhecido"


# --------------------- ROOT ---------------------

@app.get("/")
def root():
    return {"message": "YOUVISA API running"}


# --------------------- HEALTH ---------------------

@app.get("/health")
def health_check():
    return {"status": "ok"}


# --------------------- UPLOAD ---------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    file_extension = file.filename.split(".")[-1].lower()

    is_image = file_extension in ["jpg", "jpeg", "png"]
    is_pdf = file_extension == "pdf"

    doc_type = detectar_tipo_documento(file.filename)

    # BLOQUEIA nome inválido
    if doc_type == "desconhecido":
        raise HTTPException(
            status_code=400,
            detail="Tipo de documento não reconhecido. Use nomes como passaporte, comprovante_residencia, comprovante_financeiro ou formulario."
        )

    doc_id = str(uuid.uuid4())

    # Salva o arquivo em disco primeiro (para validação visual em imagens)
    ensure_uploads_dir()
    safe_ext = file_extension if file_extension in ["jpg", "jpeg", "png", "pdf"] else "bin"
    saved_filename = f"{doc_id}.{safe_ext}"
    file_path = os.path.join(UPLOADS_DIR, saved_filename)
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Validação: imagem → validação visual com OpenCV; PDF/outros → pendente
    if is_image:
        valid, reason = validate_image(file_path)
        status = DocumentStatus.CONCLUIDO if valid else DocumentStatus.PENDENTE
    elif is_pdf:
        status = DocumentStatus.PENDENTE
        reason = "Arquivo não é imagem válida."
    else:
        status = DocumentStatus.PENDENTE
        reason = "Formato de arquivo não suportado."

    document = Document(
        id=doc_id,
        filename=file.filename,
        type=doc_type,
        status=status,
        created_at=datetime.utcnow().isoformat(),
        validation_reason=reason
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO documents (id, filename, type, status, created_at, validation_reason, file_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        document.id,
        document.filename,
        document.type,
        document.status,
        document.created_at,
        document.validation_reason,
        file_path,
    ))

    cursor.execute("""
    INSERT INTO status_events (document_id, status_anterior, status_novo, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        document.id,
        "AGUARDANDO_VALIDACAO",
        document.status,
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    # dispara evento
    publish("STATUS_CHANGED", document)

    # envia e-mail avisando recebimento e status
    destinatario = os.getenv("NOTIFICATION_EMAIL", "paulobqs@gmail.com")
    if status == DocumentStatus.CONCLUIDO:
        send_email(
            destinatario,
            "YOUVISA – Documento recebido e validado",
            f"Seu documento foi recebido e salvo com sucesso.\n\n"
            f"Arquivo: {file.filename}\n"
            f"Status: validado.\n"
            f"O arquivo foi armazenado no sistema."
        )
    else:
        send_email(
            destinatario,
            "YOUVISA – Documento recebido (pendente de correção)",
            f"Recebemos e salvamos seu documento.\n\n"
            f"Arquivo: {file.filename}\n"
            f"Status: pendente de correção.\n"
            f"Motivo: {reason}\n\n"
            f"Por favor, reenvie o documento conforme as orientações."
        )

    return document


# --------------------- STATUS GLOBAL ---------------------

@app.get("/status")
def get_status():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()

    # Converte sqlite3.Row em dict (compatível com Python < 3.12)
    documents = [dict(zip(row.keys(), row)) for row in rows]

    conn.close()

    tipos_obrigatorios = [
        "passaporte",
        "comprovante_residencia",
        "comprovante_financeiro",
        "formulario"
    ]

    tipos_enviados = {
        doc["type"]
        for doc in documents
        if doc["status"] == DocumentStatus.CONCLUIDO
    }

    tipos_faltando = [
        t for t in tipos_obrigatorios if t not in tipos_enviados
    ]

    if not documents:

        global_status = DocumentStatus.AGUARDANDO

    else:

        if any(doc["status"] == DocumentStatus.PENDENTE for doc in documents):

            global_status = DocumentStatus.PENDENTE

        else:

            if tipos_faltando:
                global_status = DocumentStatus.AGUARDANDO
            else:
                global_status = DocumentStatus.CONCLUIDO

    return {
        "status_global": global_status,
        "tipos_faltando": tipos_faltando,
        "documentos": documents
    }


# --------------------- EVENT SUBSCRIBE ---------------------

subscribe("STATUS_CHANGED", handle_status_change)