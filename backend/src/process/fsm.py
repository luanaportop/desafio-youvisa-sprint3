# Máquina de estados do processo

VALID_TRANSITIONS = {

    "AGUARDANDO_DOCUMENTOS": ["EM_ANALISE"],

    "EM_ANALISE": [
        "PENDENTE_CORRECAO",
        "CONCLUIDO"
    ],

    "PENDENTE_CORRECAO": [
        "EM_ANALISE"
    ],

    "CONCLUIDO": []
}


def validar_transicao(status_atual, novo_status):

    if status_atual not in VALID_TRANSITIONS:
        return False

    return novo_status in VALID_TRANSITIONS[status_atual]