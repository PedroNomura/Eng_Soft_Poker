import pytest
import requests

# Certifique-se de que o código das classes Player, PokerRoom e funções estejam no arquivo poker.py
from pokerV0 import Player, PokerRoom, salas, listar_partidas, iniciar_partida

# Teste para criar uma sala e garantir que o jogador seja adicionado corretamente
def test_criar_sala():
    jogador = Player('victor', 1000)
    sala = jogador.criar_sala('sala1', 5, 10)
    # Verifica se a sala foi criada corretamente
    assert sala.nome == 'sala1'
    assert sala.small_blind == 5
    assert sala.big_blind == 10
    assert len(sala.players) == 1
    assert jogador in sala.players
    assert jogador.indice_sala == 0

# Teste para entrar em uma sala existente
def test_entrar_sala():
    jogador2 = Player('joao', 2000)
    entrou = jogador2.entrar_sala('sala1')
    
    assert entrou == True
    assert jogador2 in salas[0].players

# Teste para coletar cartas de um jogador
def test_coletar_cartas():
    jogador2 = Player('joao', 2000)
    deck = requests.get(https://www.deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1).json()['deck_id']
    jogador2.coletar_cartas(deck)
    assert len(jogador2.cards) == 2
    assert isinstance(jogador2.cards[0], dict)  # Verifica se as cartas são dicionários
    assert 'value' in jogador2.cards[0]  # Verifica se a carta possui a chave 'value'

# Teste para iniciar uma partida
def test_iniciar_partida():
    # Inicia a partida
    partida_iniciada = iniciar_partida(0)
    
    assert partida_iniciada == True
    assert len(salas[0].players) == 2
    assert len(salas[0].flop) == 3  # Verifica se o flop foi distribuído
    assert len(salas[0].turn) == 1  # Verifica se o turn foi distribuído
    assert len(salas[0].river) == 1  # Verifica se o river foi distribuído

# Teste para listar as partidas
def test_listar_partidas():
    jogador = Player('victor', 1000)
    jogador.criar_sala('sala2', 5, 10)
    
    partidas = listar_partidas()
    
    assert 2 == len(partidas)
    assert partidas[1].nome == 'sala2'

