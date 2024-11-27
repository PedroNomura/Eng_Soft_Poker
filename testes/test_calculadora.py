import pytest
from calculadora import soma

def test_soma():
    # Teste básico de soma
    assert soma(1, 2) == 3

    # Testando com números negativos
    assert soma(-1, -1) == -2

    # Testando com zeros
    assert soma(0, 0) == 0

    # Testando com números grandes
    assert soma(1000, 2000) == 3000
