from fastapi import FastAPI, File, UploadFile, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

# 1. Imports dos seus modelos e serviços
from models.document import Document, DocumentStatus
from nlp.gemini_service import gerar_resposta
from database.init_db import init_db
from database.db import get_connection
from document_validation import validate_image
from events.event_bus import publish, subscribe
from notifications.status_notification import handle_status_change

# Carrega variáveis de ambiente
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# 2. Inicialização do App 
app = FastAPI(
    title="YOUVISA Sprint 3 - Backend",
    version="1.0.0"
)

# 3. Inicialização do Banco e Pastas
init_db()
UPLOADS_DIR = os.path.join(os.path.dirname(__file__), "uploads")

def ensure_uploads_dir():
    os.makedirs(UPLOADS_DIR, exist_ok=True)

ensure_uploads_dir()

# 4. Middleware (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Funções Auxiliares
def detectar_tipo_documento(filename: str) -> str:
    name = filename.lower()
    if "passaporte" in name or "passport" in name:
        return "passaporte"
    if "residencia" in name or "residência" in name or "endereco" in name or "endereço" in name:
        return "comprovante_residencia"
    if "financeiro" in name or "renda" in name or "banc" in name:
        return "comprovante_financeiro"
    if "formulario" in name:
        return "formulario"
    return "desconhecido"

# --------------------- ROTAS GET  ---------------------

@app.get("/")
def root():
    return {"message": "YOUVISA API running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/status")
def get_status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
    rows = cursor.fetchall()
    documents = [dict(zip(row.keys(), row)) for row in rows]
    conn.close()

    tipos_obrigatorios = ["passaporte", "comprovante_residencia", "comprovante_financeiro", "formulario"]
    tipos_enviados = {doc["type"] for doc in documents if doc["status"] == "CONCLUIDO"}
    tipos_faltando = [t for t in tipos_obrigatorios if t not in tipos_enviados]

    # Lógica de Status Global
    if not documents:
        global_status = "AGUARDANDO_DOCUMENTOS"
    elif any(doc["status"] == "PENDENTE_CORRECAO" for doc in documents):
        global_status = "PENDENTE_CORRECAO"
    elif tipos_faltando:
        global_status = "EM_ANALISE"
    else:
        global_status = "CONCLUIDO"

    return {
        "status_global": global_status,
        "tipos_faltando": tipos_faltando,
        "documentos": documents
    }

# --------------------- ROTAS POST (Upload e Chat) ---------------------

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    is_image = file_extension in ["jpg", "jpeg", "png"]
    
    doc_type = detectar_tipo_documento(file.filename)

    if doc_type == "desconhecido":
        raise HTTPException(status_code=400, detail="Tipo de documento não reconhecido.")

    doc_id = str(uuid.uuid4())
    ensure_uploads_dir()
    
    saved_filename = f"{doc_id}.{file_extension}"
    file_path = os.path.join(UPLOADS_DIR, saved_filename)
    
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # 1. Validação Técnica (Visão Computacional)
    reason = ""
    if is_image:
        valid, reason = validate_image(file_path)
        status_proposto = DocumentStatus.CONCLUIDO if valid else DocumentStatus.PENDENTE_CORRECAO
    else:
        status_proposto = DocumentStatus.PENDENTE_CORRECAO
        reason = "Formato inválido. Use JPG ou PNG."

    # 2. VERIFICAÇÃO DA FSM
    from process.fsm import validar_transicao
    status_base = "AGUARDANDO_DOCUMENTOS"
    
    if not validar_transicao(status_base, status_proposto.value):
        status_proposto = DocumentStatus.AGUARDANDO_VALIDACAO

    # 3. Criação e Persistência
    document = Document(
        id=doc_id,
        filename=file.filename,
        type=doc_type,
        status=status_proposto,
        created_at=datetime.utcnow().isoformat(),
        validation_reason=reason,
        file_path=file_path
    )

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO documents (id, filename, type, status, created_at, validation_reason, file_path)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (document.id, document.filename, document.type, document.status.value, 
              document.created_at, document.validation_reason, file_path))
        conn.commit()
    finally:
        conn.close()

    publish("STATUS_CHANGED", document.model_dump())
    return document

@app.post("/chat")
def chat(pergunta: str = Body(..., embed=True)):
    # Reutiliza a lógica de status para o contexto da IA
    status_data = get_status()
    contexto = f"""
    Status global: {status_data['status_global']}
    Documentos faltando: {', '.join(status_data['tipos_faltando'])}
    """
    resposta = gerar_resposta(pergunta, contexto)
    return {"resposta": resposta}

# Inscrição de eventos
subscribe("STATUS_CHANGED", handle_status_change)
