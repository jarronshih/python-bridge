import pytest
from bridge.double_dummy_solver import double_dummy_solver
from bridge.models import Board, Trump, Player, Card, CardSuit, CardRank


@pytest.mark.xfail
def test_double_dummy_solver():
    board = Board(
        north=[Card(CardSuit.SPADE, CardRank.ACE)],
        east=[Card(CardSuit.SPADE, CardRank.TWO)],
        south=[Card(CardSuit.SPADE, CardRank.THREE)],
        west=[Card(CardSuit.SPADE, CardRank.FOUR)]
    )
    trump = Trump.NO_TRUMP
    starting_player = Player.EAST
    result = 1

    assert double_dummy_solver(board, trump, starting_player) == result
