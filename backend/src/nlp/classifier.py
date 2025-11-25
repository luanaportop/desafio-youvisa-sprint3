# backend/src/nlp/classifier.py
from models.document import DocumentType


def classify_document(filename: str) -> DocumentType:
    """
    Classificação bem simples baseada apenas no nome do arquivo.
    Sprint 2: simulação de NLP / IA.
    """
    name = filename.lower()

    if "pass" in name or "passport" in name:
        return DocumentType.PASSAPORTE

    if "resid" in name or "endereco" in name:
        return DocumentType.COMPROVANTE_RESIDENCIA

    if "renda" in name or "banco" in name or "finance" in name:
        return DocumentType.COMPROVANTE_FINANCEIRO

    if "form" in name or "youvisa" in name or "ds160" in name:
        return DocumentType.FORMULARIO_YOUVISA

    return DocumentType.DESCONHECIDO

