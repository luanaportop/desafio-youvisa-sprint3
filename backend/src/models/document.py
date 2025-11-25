# backend/src/models/document.py
from enum import Enum
from datetime import datetime
from pydantic import BaseModel


class DocumentType(str, Enum):
    PASSAPORTE = "passaporte"
    COMPROVANTE_RESIDENCIA = "comprovante_residencia"
    COMPROVANTE_FINANCEIRO = "comprovante_financeiro"
    FORMULARIO_YOUVISA = "formulario_youvisa"
    DESCONHECIDO = "desconhecido"


class DocumentStatus(str, Enum):
    AGUARDANDO_VALIDACAO = "AGUARDANDO_VALIDACAO"
    PENDENTE_CORRECAO = "PENDENTE_CORRECAO"
    CONCLUIDO = "CONCLUIDO"


class Document(BaseModel):
    id: str
    filename: str
    type: DocumentType
    status: DocumentStatus
    created_at: datetime
    validation_reason: str | None = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
