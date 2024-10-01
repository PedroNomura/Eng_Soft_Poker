import requests
from itertools import combinations
from pokerlib.enums import Rank, Suit
from pokerlib import HandParser

salas = []
valores = {
            '2': 2, '3': 3, '4': 4, '5': 5,
            '6': 6, '7': 7, '8': 8, '9': 9,
            'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14
        }

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
# ---------------------------------------------------------------------------------------------------------------------------------------------
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

    def verificar_ganhador(self):
        biblis = {
            'A': Rank.ACE, '2': Rank.TWO, '3': Rank.THREE, 
            '4': Rank.FOUR, '5': Rank.FIVE, '6': Rank.SIX,
            '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE,
            '0': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN,
            'K': Rank.KING, 'S': Suit.SPADE, 'C':Suit.CLUB, 'H': Suit.HEART, 'D' : Suit.DIAMOND
        }
        vencedor = None
        cartas_vencedor = None
        cartas_mesa = self.flop + self.turn + self.river
        for player in self.players:
            all_cards = player.cards + cartas_mesa
            card_strings = [card['code'] for card in all_cards]
            cartas_jogador = HandParser([])
            for card in card_strings:
                carta = [(biblis[card[0]],biblis[card[1]])]
                cartas_jogador += carta
            print(cartas_jogador.handenum)
            if vencedor is None or cartas_jogador > cartas_vencedor:
                cartas_vencedor = cartas_jogador
                vencedor = player
        return vencedor


    def start(self): # working process
        print(f"deck_id: {self.deck}")
        BB = self.players[len(self.players)-1]
        for i, player in enumerate(self.players):
            player.coletar_cartas(self.deck)
            print(f"player {i}:\n {player.cards[0]['code']} {player.cards[1]['code']}\n\n")

        for player in self.players:
            player.realizar_acao('check')
        self.flop = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=3").json()['cards']
        flopis = ""
        for card in self.flop:
            flopis += card['code'] + ' '
        print(f"flop: {flopis}\n\n")

        for player in self.players:
            player.realizar_acao('check')
        self.turn = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json()['cards']
        print(f"turn: {self.turn[0]['code']}\n\n")

        for player in self.players:
            player.realizar_acao('check')
        self.river = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json()['cards']
        print(f"river: {self.river[0]['code']}\n\n")

        vencedor = self.verificar_ganhador()
        if vencedor:
            print(f"Vencedor da rodada é {vencedor.nome}")
        else:
            print("Não foi possível determinar um vencedor.")
        self.players = self.players[1:] +[self.players[0]]
        self.deck = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/return/")
        self.deck = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/shuffle/")
        return True

# ------------------------------------------------------------------------------------------------------------------------------------------------
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

jogador = Player('victor', 1000)
jogador2 = Player('joao',2000)
sala_jogador = jogador.criar_sala('sala1',5,10)
jogador2.entrar_sala("sala1")
sala_jogador.start()

