# backend/src/models/models.py

from enum import Enum
from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    PASSAPORTE = "passaporte"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    COMPROVANTE_FINANCEIRO = "comprovante_financeiro"
    FORMULARIO_YOUVISA = "formulario_youvisa"
    DESCONHECIDO = "desconhecido"


class DocumentStatus(str, Enum):
    EM_VALIDACAO = "em_validacao"
    VALIDO = "valido"
    PENDENTE_CORRECAO = "pendente_correcao"


class ProcessStatus(str, Enum):
    AGUARDANDO_DOCUMENTOS = "AGUARDANDO_DOCUMENTOS"
    EM_ANALISE = "EM_ANALISE"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"


class Document(BaseModel):
    id: str
    filename: str
    tipo: DocumentType = DocumentType.DESCONHECIDO
    status: DocumentStatus = DocumentStatus.EM_VALIDACAO
    motivo_invalido: Optional[str] = None
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class ProcessState(BaseModel):
    """
    Representa o processo de solicitação de visto de UM usuário.
    Na Sprint 2 vamos simular sempre um único processo ativo.
    """
    processo_id: str
    status: ProcessStatus = ProcessStatus.AGUARDANDO_DOCUMENTOS
    documentos: Dict[str, Document] = Field(default_factory=dict)
