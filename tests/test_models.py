from bridge.models import Trick, Trump, Player, Card, CardSuit, CardRank


def test_trick():
    trick = Trick(trump=Trump.NO_TRUMP, starting_player=Player.EAST)

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.KING))
    assert t is None
    assert trick.winner == Player.EAST

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.TWO))
    assert t is None
    assert trick.winner == Player.EAST

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.ACE))
    assert t is None
    assert trick.winner == Player.WEST

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.THREE))
    assert t is Player.WEST
    assert trick.winner == Player.WEST
