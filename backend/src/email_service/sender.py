from models.document import DocumentStatus

def send_notification(document_data: dict) -> None:
    """
    Simula envio de e-mail via SMTP.
    Recebe um dicionário contendo os dados do documento.
    """
    # Acessando os dados via dicionário para evitar o AttributeError
    status = document_data.get("status")
    filename = document_data.get("filename")
    reason = document_data.get("validation_reason", "Não especificado")

    # Garante que estamos comparando o valor em string do status
    status_value = status.value if hasattr(status, "value") else str(status)

    if status_value == DocumentStatus.CONCLUIDO.value:
        subject = "YOUVISA – Documento validado"
        body = (
            f"Seu documento '{filename}' foi validado com sucesso.\n"
            f"Status: {status_value}"
        )
    else:
        subject = "YOUVISA – Documento precisa de correção"
        body = (
            f"Seu documento '{filename}' NÃO passou na validação.\n"
            f"Motivo: {reason}\n"
            f"Status: {status_value}"
        )

    print("\n========== EMAIL SIMULADO ==========")
    print(f"Assunto: {subject}")
    print(body)
    print("====================================\n")
