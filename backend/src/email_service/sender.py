# backend/src/email_service/sender.py
from models.document import Document, DocumentStatus


def send_notification(document: Document) -> None:
    """
    Simula envio de e-mail via SMTP.
    Sprint 2: apenas loga a mensagem no console.
    """

    if document.status == DocumentStatus.CONCLUIDO:
        subject = "YOUVISA – Documento validado"
        body = (
            f"Seu documento '{document.filename}' foi validado com sucesso.\n"
            f"Status: {document.status.value}"
        )
    else:
        subject = "YOUVISA – Documento precisa de correção"
        body = (
            f"Seu documento '{document.filename}' NÃO passou na validação.\n"
            f"Motivo: {document.validation_reason}\n"
            f"Status: {document.status.value}"
        )

    print("\n========== EMAIL SIMULADO ==========")
    print(f"Assunto: {subject}")
    print(body)
    print("====================================\n")

