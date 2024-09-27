import pytest
from poker_g import criar_partida, realizar_acao, PokerRoom

@pytest.fixture
def setup_salas():
    global salas
    salas = []
    sala = criar_partida("Teste Poker", big_blind=50, small_blind=25)
    salas.append(sala)

    # Adicione jogadores à sala para os testes
    sala.adicionar_jogador("Jogador 1")  # Adiciona um jogador
    sala.adicionar_jogador("Jogador 2")  # Adiciona outro jogador

    return sala

def test_criar_partida(setup_salas):
    sala = setup_salas
    assert sala.name == "Teste Poker"
    assert sala.big_blind == 50
    assert sala.small_blind == 25
    assert len(salas) == 1

def test_realizar_acao_check(setup_salas):
    sala = setup_salas
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0  # Verifica se há jogadores

def test_realizar_acao_bet(setup_salas):
    sala = setup_salas
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0
    sucesso = realizar_acao(1, 1, "bet", valor=100)
    assert sucesso is True

def test_realizar_acao_fold(setup_salas):
    sala = setup_salas
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0
    sucesso = realizar_acao(1, 1, "fold")
    assert sucesso is True
