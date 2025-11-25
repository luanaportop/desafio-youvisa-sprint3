# backend/src/vision/validator.py
import cv2
import numpy as np
from models.document import DocumentType


def validate_document(content: bytes, doc_type: DocumentType) -> tuple[bool, str]:
    """
    Validação visual simples com OpenCV.
    Sprint 2: simulação — checa se a imagem abre e se tem uma resolução mínima.
    """
    try:
        # converte bytes -> imagem OpenCV
        nparr = np.frombuffer(content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return False, "Arquivo não é uma imagem válida"

        h, w, _ = img.shape

        # resolução mínima bem simples
        if h < 300 or w < 300:
            return False, "Resolução muito baixa (mínimo 300x300)"

        # aqui poderíamos ter regras específicas por tipo de documento
        # (proporção, região de interesse, etc.)
        return True, "Documento válido (validação básica simulada)"

    except Exception as e:
        return False, f"Erro ao validar documento: {e}"

