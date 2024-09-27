import poker

salas = []

def criar_partida(nome_sala, big_blind, small_blind):
    sala = PokerRoom(name=nome_sala, seats=4, big_blind=big_blind, small_blind=small_blind)
    salas.append(sala)
    print(f"Partida '{nome_sala}' criada com sucesso!")
    return sala

def listar_partidas():
    if not salas:
        print("Nenhuma partida disponível no momento.")
    else:
        print("Partidas disponíveis:")
        for idx, sala in enumerate(salas):
            print(f"{idx + 1}. Nome: {sala.name}, Cadeiras: {sala.seats}, Blinds: {sala.big_blind}/{sala.small_blind}")

def iniciar_partida(indice_sala):
    try:
        sala = salas[indice_sala - 1]
        sala.start()
        print(f"Partida '{sala.name}' iniciada com sucesso!")
        return True
    except IndexError:
        print(f"Erro: Não existe uma partida no índice {indice_sala}.")
        return False

def realizar_acao(indice_sala, indice_jogador, acao, valor=None):
    try:
        sala = salas[indice_sala - 1]
        jogador = sala.players[indice_jogador - 1]
        
        if acao == 'bet' and valor:
            jogador.bet(valor)
            print(f"Jogador {jogador.name} apostou {valor}.")
            return True
        elif acao == 'check':
            jogador.check()
            print(f"Jogador {jogador.name} deu check.")
            return True
        elif acao == 'fold':
            jogador.fold()
            print(f"Jogador {jogador.name} deu fold.")
            return True
        else:
            print("Ação inválida ou valor não especificado.")
            return False
    except IndexError:
        print(f"Erro: Não existe a partida ou jogador no índice fornecido.")
        return False
