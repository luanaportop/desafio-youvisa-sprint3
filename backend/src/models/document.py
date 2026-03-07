from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class DocumentType(str, Enum):
    PASSAPORTE = "passaporte"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    COMPROVANTE_FINANCEIRO = "comprovante_financeiro"
    FORMULARIO = "formulario" 
    DESCONHECIDO = "desconhecido"

class DocumentStatus(str, Enum):
    """Estados individuais de cada documento"""
    AGUARDANDO_VALIDACAO = "AGUARDANDO_VALIDACAO"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"

class ProcessStatus(str, Enum):
    """Estados globais do processo"""
    AGUARDANDO_DOCUMENTOS = "AGUARDANDO_DOCUMENTOS"
    EM_ANALISE = "EM_ANALISE"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"

class Document(BaseModel):
    id: str
    filename: str
    type: str # Mudado para str para facilitar a comparação no banco
    status: DocumentStatus
    created_at: str # Mudado para str para simplificar o Pydantic com SQLite
    validation_reason: Optional[str] = None
    file_path: Optional[str] = None

    class Config:
        from_attributes = True
