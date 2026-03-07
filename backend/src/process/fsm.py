# Máquina de estados do processo - YOUVISA Sprint 3

VALID_TRANSITIONS = {
    # O processo começa aqui. Ao receber um documento, ele pode ir para análise
    # ou direto para pendência/concluído se a validação automática rodar no upload.
    "AGUARDANDO_DOCUMENTOS": [
        "EM_ANALISE", 
        "PENDENTE_CORRECAO", 
        "CONCLUIDO"
    ],

    "EM_ANALISE": [
        "PENDENTE_CORRECAO",
        "CONCLUIDO"
    ],

    "PENDENTE_CORRECAO": [
        "EM_ANALISE",
        "CONCLUIDO" # Permitimos ir direto para concluído se o reenvio for perfeito
    ],

    "CONCLUIDO": [] # Estado final
}

def validar_transicao(status_atual: str, novo_status: str):
    # Se os status forem iguais, permitimos (ex: atualizar dados sem mudar fase)
    if status_atual == novo_status:
        return True

    if status_atual not in VALID_TRANSITIONS:
        return False

    return novo_status in VALID_TRANSITIONS[status_atual]
