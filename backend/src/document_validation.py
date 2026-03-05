# Validação visual automatizada com OpenCV.
# Verifica resolução mínima, proporção e nitidez (blur) da imagem.

import cv2
import os
from typing import Tuple

# Resolução mínima (largura e altura) para documento legível
MIN_WIDTH = 400
MIN_HEIGHT = 400

# Proporção aceitável (largura/altura) para documento – evita linhas ou quadrados estranhos
MIN_ASPECT_RATIO = 0.25   # ex.: retrato estreito
MAX_ASPECT_RATIO = 3.0   # ex.: paisagem larga

# Nitidez: variância do Laplacian abaixo disso = imagem muito borrada
MIN_LAPLACIAN_VARIANCE = 100


def validate_image(file_path: str) -> Tuple[bool, str]:
    """
    Valida a imagem com OpenCV.
    Retorna (válido: bool, mensagem: str).
    """
    if not os.path.isfile(file_path):
        return False, "Arquivo não encontrado."

    try:
        img = cv2.imread(file_path)
        if img is None:
            return False, "Não foi possível ler a imagem. Verifique o formato (JPEG/PNG)."

        h, w = img.shape[:2]

        # 1. Resolução mínima
        if w < MIN_WIDTH or h < MIN_HEIGHT:
            return False, (
                f"Resolução insuficiente ({w}x{h} px). "
                f"Mínimo recomendado: {MIN_WIDTH}x{MIN_HEIGHT} px para documento legível."
            )

        # 2. Proporção (layout de documento)
        aspect = w / h if h > 0 else 0
        if aspect < MIN_ASPECT_RATIO or aspect > MAX_ASPECT_RATIO:
            return False, (
                f"Proporção da imagem fora do esperado para documento "
                f"(atual: {aspect:.2f}). Use foto em formato retrato ou paisagem de documento."
            )

        # 3. Nitidez (detecção de blur)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < MIN_LAPLACIAN_VARIANCE:
            return False, (
                f"Imagem muito borrada ou de baixa qualidade. "
                f"Tire uma foto mais nítida do documento."
            )

        return True, "Documento válido (validação visual: resolução, proporção e nitidez OK)."

    except Exception as e:
        return False, f"Erro na validação da imagem: {str(e)}"
