from fastapi import UploadFile, BackgroundTasks
from .pipeline import PipelineAutomacao


# Instância única do pipeline para toda a aplicação
_pipeline = PipelineAutomacao()


async def process_document(
    file: UploadFile,
    background_tasks: BackgroundTasks,
):
    """
    Função chamada pelo main.py para processar um documento.
    """
    return await _pipeline.process_document(file, background_tasks)


def get_process_status() -> dict:
    """
    Função chamada pelo main.py para obter status geral.
    """
    return _pipeline.get_process_status()
