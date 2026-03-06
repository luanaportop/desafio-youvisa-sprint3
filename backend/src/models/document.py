from enum import Enum
from datetime import datetime
from typing import Optional, Dict, List
from pydantic import BaseModel, Field

# --- ENUMS (A base da nossa Máquina de Estados) ---

class DocumentType(str, Enum):
    PASSAPORTE = "passaporte"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    COMPROVANTE_FINANCEIRO = "comprovante_financeiro"
    FORMULARIO_YOUVISA = "formulario" # Padronizado com o detectar_tipo_documento do main.py
    DESCONHECIDO = "desconhecido"

class DocumentStatus(str, Enum):
    """Estados individuais de cada documento"""
    AGUARDANDO_VALIDACAO = "AGUARDANDO_VALIDACAO"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"

class ProcessStatus(str, Enum):
    """Estados globais do processo (Sprint 3 FSM)"""
    AGUARDANDO_DOCUMENTOS = "AGUARDANDO_DOCUMENTOS"
    EM_ANALISE = "EM_ANALISE"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"

# --- MODELOS DE DADOS (Pydantic) ---

class Document(BaseModel):
    """Representa um documento individual no sistema"""
    id: str
    filename: str
    type: DocumentType
    status: DocumentStatus = DocumentStatus.AGUARDANDO_VALIDACAO
    created_at: datetime = Field(default_factory=datetime.utcnow)
    validation_reason: Optional[str] = None
    file_path: Optional[str] = None # Adicionado para rastreabilidade do arquivo físico

    class Config:
        # Garante que o JSON de saída formate a data corretamente
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        from_attributes = True # Permite converter de registros do SQLite (Row) para Document

class ProcessState(BaseModel):
    """
    Representa o estado completo da solicitação de visto.
    Essencial para alimentar o contexto da IA Generativa.
    """
    processo_id: str
    status_global: ProcessStatus = ProcessStatus.AGUARDANDO_DOCUMENTOS
    documentos: List[Document] = []
    tipos_faltando: List[DocumentType] = []

    class Config:
        from_attributes = True
