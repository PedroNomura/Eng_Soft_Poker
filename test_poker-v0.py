import pytest
frrom poker-v0 import criar_partida, listar_partidas, iniciar_partida, realizar_acao

def test_criar_partida():
    sala = criar_partida("Teste Poker", big_blind=50, small_blind=25)
    assert sala.name == "Teste Poker"
    assert sala.big_blind == 50
    assert sala.small_blind == 25
    assert len(salas) == 1

def test_listar_partidas():
    partidas = listar_partidas()
    assert len(partidas) == 1
    assert partidas[0].name == "Teste Poker"

def test_iniciar_partida():
    sucesso = iniciar_partida(1)
    assert sucesso is True

def test_realizar_acao_check():
    sala = salas[0]
    sala.add_player(name="Jogador 1", stack=1000)
    sucesso = realizar_acao(1, 1, "check")
    assert sucesso is True

def test_realizar_acao_bet():
    sucesso = realizar_acao(1, 1, "bet", valor=100)
    assert sucesso is True

def test_realizar_acao_fold():
    sucesso = realizar_acao(1, 1, "fold")
    assert sucesso is True
