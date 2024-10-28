from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Lista para armazenar as salas de poker
salas = []

class Player:
    def __init__(self, nome, chips):
        self.nome = nome
        self.fichas = chips
        self.cards = []
        self.indice_sala = -1

    def criar_sala(self, nome_sala, small_blind, big_blind):
        nova_sala = PokerRoom(nome_sala, 4, small_blind, big_blind)
        salas.append(nova_sala)
        self.indice_sala = len(salas) - 1
        nova_sala.players.append(self)
        return nova_sala

    def entrar_sala(self, indice_sala):
        if 0 <= indice_sala < len(salas):
            sala = salas[indice_sala]
            if len(sala.players) < sala.seats:
                self.indice_sala = indice_sala
                sala.players.append(self)
                self.coletar_cartas(sala.deck)
                return True
        return False

    def coletar_cartas(self, deck_id):
        url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2"
        self.cards = requests.get(url).json().get('cards', [])


class PokerRoom:
    def __init__(self, nome, seats, small_blind, big_blind):
        self.nome = nome
        self.seats = seats
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.players = []
        self.deck = requests.get("https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1").json()['deck_id']
        self.pot = 0
        self.flop = []
        self.turn = []
        self.river = []

    def iniciar_rodada(self):
        self.flop = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=3").json().get('cards', [])
        self.turn = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json().get('cards', [])
        self.river = requests.get(f"https://deckofcardsapi.com/api/deck/{self.deck}/draw/?count=1").json().get('cards', [])


# Criação do jogador e de algumas salas para teste
jogador = Player('Victor', 1000)
jogador.criar_sala('Sala 1', 5, 10)
jogador.criar_sala('Sala 2', 10, 20)


@app.route('/')
def home():
    return render_template('mesas.html', salas=salas)


@app.route('/mesa/<int:indice_sala>')
def entrar_mesa(indice_sala):
    if jogador.entrar_sala(indice_sala):
        sala = salas[indice_sala]
        sala.iniciar_rodada()
        return render_template('mesa.html', sala=sala, jogador=jogador)
    else:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


