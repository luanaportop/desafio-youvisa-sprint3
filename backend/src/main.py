from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
from models.document import Document, DocumentStatus, DocumentType
import uuid
import os
import smtplib
from dotenv import load_dotenv
from nlp.gemini_service import gerar_resposta
from fastapi import Body


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

    if doc_type == "desconhecido":
        raise HTTPException(
            status_code=400,
            detail="Tipo de documento não reconhecido. Use nomes como passaporte, comprovante_residencia, comprovante_financeiro ou formulario."
        )

    doc_id = str(uuid.uuid4())
    ensure_uploads_dir()
    
    safe_ext = file_extension if file_extension in ["jpg", "jpeg", "png", "pdf"] else "bin"
    saved_filename = f"{doc_id}.{safe_ext}"
    file_path = os.path.join(UPLOADS_DIR, saved_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Definição do status proposto
    if is_image:
        valid, reason = validate_image(file_path)
        status_proposto = DocumentStatus.CONCLUIDO if valid else DocumentStatus.PENDENTE_CORRECAO
    elif is_pdf:
        status_proposto = DocumentStatus.PENDENTE_CORRECAO
        reason = "Arquivo não é imagem válida (PDF não aceito)."
    else:
        status_proposto = DocumentStatus.PENDENTE_CORRECAO
        reason = "Formato de arquivo não suportado."

    # --- VERIFICAÇÃO DA FSM ---
    from process.fsm import validar_transicao
    status_inicial = "AGUARDANDO_DOCUMENTOS"
    
    if not validar_transicao(status_inicial, status_proposto.value):
        raise HTTPException(
            status_code=400,
            detail=f"Transição de estado inválida: {status_inicial} -> {status_proposto.value}"
        )

    # Criação do objeto Document (Pydantic)
    document = Document(
        id=doc_id,
        filename=file.filename,
        type=doc_type,
        status=status_proposto,
        created_at=datetime.utcnow().isoformat(),
        validation_reason=reason
    )

    # Persistência no Banco de Dados
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO documents (id, filename, type, status, created_at, validation_reason, file_path)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        document.id,
        document.filename,
        str(document.type.value),
        str(document.status.value),
        document.created_at,
        document.validation_reason,
        file_path,
    ))

    cursor.execute("""
    INSERT INTO status_events (document_id, status_anterior, status_novo, timestamp)
    VALUES (?, ?, ?, ?)
    """, (
        document.id,
        "AGUARDANDO_DOCUMENTOS",
        str(document.status.value),
        datetime.utcnow().isoformat()
    ))

    conn.commit()
    conn.close()

    # Dispara evento para o Event Bus
    publish("STATUS_CHANGED", document.model_dump())

    # Notificação por e-mail (usando status_proposto)
    destinatario = os.getenv("NOTIFICATION_EMAIL", "paulobqs@gmail.com")
    if status_proposto == DocumentStatus.CONCLUIDO:
        send_email(
            destinatario,
            "YOUVISA – Documento recebido e validado",
            f"Seu documento foi recebido e validado com sucesso.\n\nArquivo: {file.filename}"
        )
    else:
        send_email(
            destinatario,
            "YOUVISA – Documento com pendência",
            f"Recebemos seu documento, mas ele precisa de correção.\n\nMotivo: {reason}"
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
        global_status = DocumentStatus.AGUARDANDO_VALIDACAO

    else:
        if any(doc["status"] == DocumentStatus.PENDENTE_CORRECAO for doc in documents):
            global_status = DocumentStatus.PENDENTE_CORRECAO

        else:
            if tipos_faltando:
                global_status = DocumentStatus.AGUARDANDO_VALIDACAO
            else:
                global_status = DocumentStatus.CONCLUIDO

    return {
        "status_global": global_status,
        "tipos_faltando": tipos_faltando,
        "documentos": documents
    }


# ----------------------CONTEXTO DO PROCESSO -------------------

def montar_contexto_processo():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()

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
        status_global = DocumentStatus.AGUARDANDO_VALIDACAO
    else:
        if any(doc["status"] == DocumentStatus.PENDENTE_CORRECAO for doc in documents):
            status_global = DocumentStatus.PENDENTE_CORRECAO
        else:
            if tipos_faltando:
                status_global = DocumentStatus.AGUARDANDO_VALIDACAO
            else:
                status_global = DocumentStatus.CONCLUIDO

    return {
        "status_global": status_global,
        "tipos_faltando": tipos_faltando,
        "documentos": documents
    }


# --------------------- CHAT IA GENERATIVA ---------------------

@app.post("/chat")
def chat(pergunta: str = Body(..., embed=True)):
    contexto_dict = montar_contexto_processo()

    documentos_texto = "\n".join(
        [
            f"- {doc['filename']} | tipo={doc['type']} | status={doc['status']}"
            for doc in contexto_dict["documentos"]
        ]
    )

    if not documentos_texto:
        documentos_texto = "Nenhum documento enviado até o momento."

    tipos_faltando = ", ".join(contexto_dict["tipos_faltando"])
    if not tipos_faltando:
        tipos_faltando = "nenhum"

    contexto = f"""
Status global do processo: {contexto_dict['status_global']}
Tipos de documentos faltando: {tipos_faltando}

Documentos registrados no sistema:
{documentos_texto}
"""

    resposta = gerar_resposta(pergunta, contexto)

    return {"resposta": resposta}


# --------------------- EVENT SUBSCRIBE ---------------------

subscribe("STATUS_CHANGED", handle_status_change) 
