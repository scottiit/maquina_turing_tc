# 1. Parâmetros da Máquina
alfabeto = ['a', 'b', 'c']
estados_finais = ['q_aceita']
branco = 'E'

# 2. Função de Transição (delta)
# (estado_atual, simbolo_lido) -> (novo_estado, novo_simbolo, direcao)
transicoes = {
    ('q0', '*'): ('q1', '*', 'R'),
    ('q1', 'a'): ('q2', 'a', 'R'), # OBRIGA a ler pelo menos um 'a' para ir pro q2
    ('q2', 'a'): ('q2', 'a', 'R'), # q2 permite ler infinitos outros 'a's
    ('q2', 'E'): ('q_aceita', 'E', 'L') 
}

transicoes_paridade = {
    ('q0', '*'): ('q_par', '*', 'R'), # Começa no estado par
    
    # Se está par e lê 'a', vai para ímpar
    ('q_par', 'a'): ('q_impar', 'a', 'R'),
    ('q_par', 'b'): ('q_par', 'b', 'R'),
    ('q_par', 'c'): ('q_par', 'c', 'R'),
    ('q_par', 'E'): ('q_aceita', 'E', 'R'), # Se terminar no par, ACEITA
    
    # Se está ímpar e lê 'a', volta para par
    ('q_impar', 'a'): ('q_par', 'a', 'R'),
    ('q_impar', 'b'): ('q_impar', 'b', 'R'),
    ('q_impar', 'c'): ('q_impar', 'c', 'R')
    # Não tem transição de 'q_impar' para 'E'. Se chegar no vazio sendo ímpar, a máquina trava (REJEITA).
}

transicoes_an_bn = {
    ('q0', '*'): ('q1', '*', 'R'),
    
# q1: Procura 'a' para transformar em 'X'
    ('q1', 'E'): ('q_aceita', 'E', 'R'), # Se ler o vazio logo de cara (n=0), ACEITA
    ('q1', 'a'): ('q2', 'X', 'R'),
    ('q1', 'Y'): ('q4', 'Y', 'R'),
    
    # q2: Viaja para a direita até achar um 'b'
    ('q2', 'a'): ('q2', 'a', 'R'),
    ('q2', 'Y'): ('q2', 'Y', 'R'),
    ('q2', 'b'): ('q3', 'Y', 'L'), # Achou 'b', transforma em 'Y' e começa a voltar
    
    # q3: Viaja para a esquerda até achar o 'X'
    ('q3', 'a'): ('q3', 'a', 'L'),
    ('q3', 'Y'): ('q3', 'Y', 'L'),
    ('q3', 'X'): ('q1', 'X', 'R'), # Achou o 'X', dá um passo à direita e reinicia o ciclo
    
    # q4: Verifica se sobrou apenas 'Y' (nenhum 'b' sobrando)
    ('q4', 'Y'): ('q4', 'Y', 'R'),
    ('q4', 'E'): ('q_aceita', 'E', 'R')
}

transicoes_por_nome = {
    '1': ('Máquina original', transicoes),
    '2': ('Paridade de a', transicoes_paridade),
    '3': ('Linguagem a^n b^n', transicoes_an_bn)
}

# 3. Lógica do Simulador
def executar_maquina(palavra_input, transicoes_escolhidas, debug=True):
    fita = list(palavra_input)
    cabecote = 0
    estado_atual = 'q0'
    
    if debug:
        print(f"Estado Inicial: {''.join(fita)}")

    while estado_atual not in estados_finais:
        simbolo_atual = fita[cabecote]
        chave = (estado_atual, simbolo_atual)
        
        # Verifica se existe instrução para o estado e símbolo atuais
        if chave in transicoes_escolhidas:
            novo_estado, novo_simbolo, direcao = transicoes_escolhidas[chave]
            
            # Atualiza a fita e o estado
            fita[cabecote] = novo_simbolo
            estado_atual = novo_estado
            
            # Movimenta o cabeçote
            if direcao == 'R':
                cabecote += 1
                if cabecote == len(fita):
                    fita.append(branco) # Fita infinita para a direita
            elif direcao == 'L':
                cabecote -= 1
                if cabecote < 0:
                    fita.insert(0, branco) # Fita infinita para a esquerda
                    cabecote = 0
                    
            if debug:
                fita_str = "".join(fita)
                print(f"[{estado_atual}] Fita: {fita_str[:cabecote]}[{fita[cabecote]}]{fita_str[cabecote+1:]}")
        else:
            return "REJEITA" # Máquina travou por falta de transição
            
    return "ACEITA" # Chegou no estado final


def mostrar_menu_transicoes():
    print("\nEscolha a transição que deseja usar:")
    for chave, (nome, _) in transicoes_por_nome.items():
        print(f"{chave} - {nome}")
    print("Digite 'sair' para encerrar")

# --- Execução ---
while True:
    mostrar_menu_transicoes()
    escolha = input("Opção: ").strip().lower()

    if escolha == 'sair':
        break

    if escolha not in transicoes_por_nome:
        print("Opção inválida.")
        continue

    _, transicoes_escolhidas = transicoes_por_nome[escolha]

    while True:
        input_str = input("\nDigite a palavra de entrada (ou 'sair' para voltar ao menu): ").strip()
        if input_str.lower() == 'sair':
            break
        print(f"\nResultado Final: {executar_maquina(input_str, transicoes_escolhidas)}")
