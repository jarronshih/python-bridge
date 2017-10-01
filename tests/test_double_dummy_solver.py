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
    Define as https://github.com/dds-bridge/ddd/blob/develop/giblib.h
        contracts n/s/h/d/c
        leader s/e/n/w

    {name=gib2
       tricks: 1111 1111 1111 1111 1111 (max=2)
    }
    k9... jt... q...a a8...:--------------------
    """
    cases = [
        ('k9... jt... q...a a8...', '1111 1111 1111 1111 1111'),
        ('k9..2. jt...q q...a8 a8..3.', '2122 2121 2122 2222 1111'),
    ]

    for gib_string, gib_result in cases:
        board = Board.create_from_gib(gib_string)

        for trump, trump_result in zip([Trump.NO_TRUMP, Trump.SPADE, Trump.HEART, Trump.DIAMOND, Trump.CLUB], gib_result.split(' ')):
            for leader, result_string in zip([Player.SOUTH, Player.EAST, Player.NORTH, Player.WEST], trump_result):
                result = int(result_string, 16)
                assert double_dummy_solver(board, trump, leader) == result
