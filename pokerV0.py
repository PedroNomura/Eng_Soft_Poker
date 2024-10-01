import requests

salas = []

class Player:
    def __init__(self, nome, chips):
        self.nome = nome
        self.fichas = chips
        self.cards = []
        self.indice_sala = -1

    def criar_sala(self, nome_sala, small_blind, big_blind):
        nova_sala = PokerRoom(nome_sala, 4,small_blind, big_blind)
        salas.append(nova_sala)
        self.indice_sala = len(salas) - 1  # Atribui o índice correto ao jogador
        nova_sala.players.append(self)  # Adiciona o jogador à sala
        return nova_sala

    def entrar_sala(self, nome_sala):
        for sala in salas:
            if len(sala.players) < sala.seats and sala.nome == nome_sala:
                self.indice_sala = salas.index(sala)
                sala.players.append(self)
                return True
        return False

    def coletar_cartas(self, deck_id):
        url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2"
        self.cards = requests.get(url).json()['cards']

    def realizar_acao(self, acao, valor=None):
        sala = salas[self.indice_sala]
        if acao == 'bet':
            sala.pot += valor
            print(f"Jogador {self.nome} apostou {valor}.")
        elif acao == 'check':
            print(f"Jogador {self.nome} deu check.")
        elif acao == 'fold':
            print(f"Jogador {self.nome} deu fold.")
        return True  # Retorne True se a ação for realizada com sucesso


class PokerRoom:
    def __init__(self, nome, seats, small_blind, big_blind):
        self.nome = nome
        self.seats = seats
        self.big_blind = big_blind
        self.small_blind = small_blind
        self.players = []

        self.deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()['deck_id']
        self.pot = 0
        self.flop = []
        self.turn = []
        self.river = []

    def adicionar_jogador(self, player):
        if len(self.players) < self.seats:
            self.players.append(player)
            player.coletar_cartas(self.deck)

    def start(self): # working process
        print(f"deck_id: {self.deck}")
        BB = self.players[len(self.players)-1]
        for player in self.players:
            player.coletar_cartas(self.deck)
        for player in self.players:
            player.realizar_acao('check')
        self.flop = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=3").json()['cards']
        for player in self.players:
            player.realizar_acao('check')
        self.turn = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json()['cards']
        for player in self.players:
            player.realizar_acao('check')
        self.river = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json()['cards']

        for i, player in enumerate(self.players):
            print(f"player {i}:\n {player.cards}\n\n")

        print(f"flop: {self.flop}\n\n")
        print(f"turn: {self.turn}\n\n")
        print(f"river: {self.river}\n\n")

        self.players = self.players[1:] +[self.players[0]]
        self.deck = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/return/")
        self.deck = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/shuffle/")
        return True

    


def listar_partidas():
    if not salas:
        print("Nenhuma partida disponível no momento.")
        return []
    else:
        print("Partidas disponíveis:")
        for idx, sala in enumerate(salas):
            print(f"{idx}. Nome: {sala.nome}, Cadeiras: {sala.seats}, Blinds: {sala.big_blind}/{sala.small_blind}, Jogadores: {len(sala.players)}")
        return salas


def iniciar_partida(indice_sala):
    try:
        sala = salas[indice_sala]
        if len(sala.players) > 1:
            sala.start()
            print(f"Partida '{sala.nome}' iniciada com sucesso!")
            return True
        else:
            print(f"Partida '{sala.nome}' não iniciada! Precisa de mais jogadores.")
            return False
    except IndexError:
        print(f"Erro: Não existe uma partida no índice {indice_sala}.")
        return False

# jogador = Player('victor', 1000)
#jogador2 = Player('joao',2000)
#sala_jogador = jogador.criar_sala('sala1',5,10)
#jogador2.entrar_sala("sala1")
#sala_jogador.start()

