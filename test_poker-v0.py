import pytest
from poker_g import criar_partida, realizar_acao, PokerRoom  # Importe a classe PokerRoom se necessário

@pytest.fixture
def setup_salas():
    global salas  # Permite modificar a lista global
    salas = []  # Reinicializa a lista de salas para cada teste
    sala = criar_partida("Teste Poker", big_blind=50, small_blind=25)
    salas.append(sala)  # Adiciona a sala à lista
    # Adicione aqui jogadores, se necessário, por exemplo:
    # sala.adicionar_jogador("Jogador 1")
    return sala  # Retorna a sala criada para uso nos testes

def test_criar_partida(setup_salas):
    sala = setup_salas
    assert sala.name == "Teste Poker"
    assert sala.big_blind == 50
    assert sala.small_blind == 25
    assert len(salas) == 1  # Agora salas deve estar definido

def test_realizar_acao_check(setup_salas):
    sala = setup_salas
    # Verifique se há jogadores na sala antes de realizar ações
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0  # Certifique-se de que a lógica está correta
    # Continue com o teste para a ação de check

def test_realizar_acao_bet(setup_salas):
    sala = setup_salas
    # Certifique-se de que há jogadores na sala
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0
    sucesso = realizar_acao(1, 1, "bet", valor=100)
    assert sucesso is True

def test_realizar_acao_fold(setup_salas):
    sala = setup_salas
    # Certifique-se de que há jogadores na sala
    assert hasattr(sala, 'jogadores') and len(sala.jogadores) > 0
    sucesso = realizar_acao(1, 1, "fold")
    assert sucesso is True
