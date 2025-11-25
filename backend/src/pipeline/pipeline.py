from uuid import uuid4
from datetime import datetime
from typing import Dict, List

from fastapi import UploadFile, BackgroundTasks

from models.document import Document, DocumentStatus, DocumentType
from nlp.classifier import classify_document
from vision.validator import validate_document
from email_service.sender import send_notification


class PipelineAutomacao:
    """
    Core do pipeline da Sprint 2.
    Mantém os documentos em memória e executa:
    - classificação (NLP)
    - validação visual (OpenCV)
    - atualização de status
    - disparo de notificação (simulada)
    """

    def __init__(self) -> None:
        # "Banco de dados" em memória
        self._documents: Dict[str, Document] = {}

    async def process_document(
        self,
        file: UploadFile,
        background_tasks: BackgroundTasks,
    ) -> Document:
        # 1) Lê conteúdo do arquivo
        content = await file.read()

        # 2) Gera ID
        doc_id = str(uuid4())

        # 3) Classifica tipo de documento (NLP / regras)
        doc_type: DocumentType = classify_document(file.filename)

        # 4) Valida imagem (visão computacional simulada)
        is_valid, reason = validate_document(content, doc_type)

        # 5) Define status
        status = (
            DocumentStatus.CONCLUIDO
            if is_valid
            else DocumentStatus.PENDENTE_CORRECAO
        )

        # 6) Cria objeto Document
        document = Document(
            id=doc_id,
            filename=file.filename,
            type=doc_type,
            status=status,
            created_at=datetime.utcnow(),
            validation_reason=reason,
        )

        # 7) Salva em memória
        self._documents[doc_id] = document

        # 8) Dispara "e-mail" em background (simulado)
        background_tasks.add_task(send_notification, document)

        return document

    def get_process_status(self) -> dict:
        """
        Retorna visão geral do processo:
        - status global
        - lista de documentos
        """
        docs: List[Document] = list(self._documents.values())

        if not docs:
            global_status = DocumentStatus.AGUARDANDO_VALIDACAO
        elif any(d.status == DocumentStatus.PENDENTE_CORRECAO for d in docs):
            global_status = DocumentStatus.PENDENTE_CORRECAO
        elif all(d.status == DocumentStatus.CONCLUIDO for d in docs):
            global_status = DocumentStatus.CONCLUIDO
        else:
            global_status = DocumentStatus.EM_ANALISE

        return {
            "global_status": global_status,
            "documents": docs,
        }

