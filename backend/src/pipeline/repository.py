# backend/src/pipeline/repository.py

from typing import Optional
from models import ProcessState, ProcessStatus


class InMemoryRepository:
    """
    Repositório simples em memória para simular persistência.
    Sprint 2 não utiliza banco de dados real — apenas simulação.
    """

    def __init__(self):
        self.process_state: Optional[ProcessState] = None

    def criar_processo(self, processo: ProcessState):
        self.process_state = processo

    def obter_processo(self) -> Optional[ProcessState]:
        return self.process_state

    def atualizar_status_global(self, novo_status: ProcessStatus):
        if self.process_state:
            self.process_state.status = novo_status

    def salvar_documento(self, doc):
        if self.process_state:
            self.process_state.documentos[doc.id] = doc
