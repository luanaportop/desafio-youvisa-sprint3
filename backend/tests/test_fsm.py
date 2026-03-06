import sys
import os

# Ajuste para o Python encontrar a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from process.fsm import validar_transicao

def testar_fluxo():
    print("\n" + "="*40)
    print("🚀 INICIANDO TESTES DA FSM YOUVISA")
    print("="*40 + "\n")

    try:
        # --- TESTES DE SUCESSO (Caminhos Felizes) ---
        
        # 1. Início do processo
        assert validar_transicao("AGUARDANDO_DOCUMENTOS", "EM_ANALISE") == True
        print("✔ TESTE 1: AGUARDANDO -> EM_ANALISE (Permitido)")

        # 2. Documento com erro sendo corrigido
        assert validar_transicao("EM_ANALISE", "PENDENTE_CORRECAO") == True
        print("✔ TESTE 2: EM_ANALISE -> PENDENTE_CORRECAO (Permitido)")

        # 3. Finalização
        assert validar_transicao("EM_ANALISE", "CONCLUIDO") == True
        print("✔ TESTE 3: EM_ANALISE -> CONCLUIDO (Permitido)")


        # --- TESTES DE SEGURANÇA (Bloqueios) ---
        
        # 4. Pular etapas (Tentativa de burlar a análise)
        assert validar_transicao("AGUARDANDO_DOCUMENTOS", "CONCLUIDO") == False
        print("✔ TESTE 4: Bloqueio AGUARDANDO -> CONCLUIDO (Correto)")

        # 5. Voltar de um estado finalizado
        assert validar_transicao("CONCLUIDO", "EM_ANALISE") == False
        print("✔ TESTE 5: Bloqueio CONCLUIDO -> EM_ANALISE (Correto)")

        print("\n" + "="*40)
        print("✅ TODOS OS TESTES PASSARAM COM SUCESSO!")
        print("="*40)

    except AssertionError as e:
        print("\n" + "!"*40)
        print("❌ FALHA NO TESTE: A FSM se comportou de forma inesperada.")
        print("!"*40)

if __name__ == "__main__":
    testar_fluxo()
