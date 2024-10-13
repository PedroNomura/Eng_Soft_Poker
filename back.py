from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista para armazenar as salas
salas = []

class Player:
    def __init__(self, nome, fichas):
        self.nome = nome
        self.fichas = fichas

class PokerRoom:
    def __init__(self, nome, seats, small_blind, big_blind):
        self.nome = nome
        self.seats = seats
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.players = []

    def adicionar_jogador(self, player):
        if len(self.players) < self.seats:
            self.players.append(player)

@app.route('/criar_sala', methods=['POST'])
def criar_sala():
    dados = request.json
    nome_sala = dados.get('nome_sala')
    seats = dados.get('seats')
    small_blind = dados.get('small_blind')
    big_blind = dados.get('big_blind')
    
    nova_sala = PokerRoom(nome_sala, seats, small_blind, big_blind)
    salas.append(nova_sala)
    return jsonify({"message": "Sala criada com sucesso!", "sala": nome_sala})

@app.route('/listar_salas', methods=['GET'])
def listar_salas():
    salas_disponiveis = [{
        "nome": sala.nome,
        "jogadores": len(sala.players),
        "max_jogadores": sala.seats,
        "small_blind": sala.small_blind,
        "big_blind": sala.big_blind
    } for sala in salas]
    return jsonify(salas_disponiveis)

if __name__ == '__main__':
    app.run(debug=True)
