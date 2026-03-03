from email_service.sender import send_notification


def handle_status_change(event):

    print("Evento recebido:", event)

    send_notification(event)