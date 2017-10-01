import itertools

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


def test_gib2():
    """
    Testcase from https://github.com/dds-bridge/ddd/blob/develop/test.gib

    {name=gib2
       tricks: 1111 1111 1111 1111 1111 (max=2)
    }
    k9... jt... q...a a8...:--------------------
    """

    board = Board.create_from_gib('k9... jt... q...a a8...')
    for trump, player in itertools.product(Trump, Player):
        assert double_dummy_solver(board, trump, player) == 1
