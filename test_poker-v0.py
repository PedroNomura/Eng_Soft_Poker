import pytest
from poker_g import criar_partida, listar_partidas, iniciar_partida, realizar_acao

salas = []  # Inicializa a lista de salas

def test_criar_partida():
    sala = criar_partida("Teste Poker", big_blind=50, small_blind=25)
    assert sala.name == "Teste Poker"
    assert sala.big_blind == 50
    assert sala.small_blind == 25
    assert len(salas) == 1  # Agora salas deve estar definido

def test_realizar_acao_check():
    sala = salas[0]  # A primeira sala deve estar disponível
    # Verifique se há jogadores na sala antes de realizar ações
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0  # Isso depende da estrutura da classe
    # Continue com o resto do seu teste...

def test_realizar_acao_bet():
    sucesso = realizar_acao(1, 1, "bet", valor=100)
    assert sucesso is True

def test_realizar_acao_fold():
    sucesso = realizar_acao(1, 1, "fold")
    assert sucesso is True

