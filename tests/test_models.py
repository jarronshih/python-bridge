from bridge.models import Trick, Trump, Player, Card, CardSuit, CardRank, Hand


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


def test_Hand_empty():
    hand = Hand()
    candidates = hand.candidate_cards()
    assert len(candidates) == 0


def test_Hand():
    SA = Card(CardSuit.SPADE, CardRank.ACE)
    SK = Card(CardSuit.SPADE, CardRank.KING)
    HA = Card(CardSuit.HEART, CardRank.ACE)
    DA = Card(CardSuit.DIAMOND, CardRank.ACE)
    hand = Hand(cards=[SA, SK, HA, DA])

    candidates = hand.candidate_cards()
    assert len(candidates) == 4

    candidates = hand.candidate_cards(CardSuit.SPADE)
    assert len(candidates) == 2

    candidates = hand.candidate_cards(CardSuit.HEART)
    assert len(candidates) == 1

    candidates = hand.candidate_cards(CardSuit.DIAMOND)
    assert len(candidates) == 1

    candidates = hand.candidate_cards(CardSuit.CLUB)
    assert len(candidates) == 4

    hand.play_card(Card(CardSuit.HEART, CardRank.ACE))
    candidates = hand.candidate_cards(CardSuit.HEART)
    assert Card(CardSuit.HEART, CardRank.ACE) not in candidates
    assert len(candidates) == 3

    hand.reverse()
    candidates = hand.candidate_cards(CardSuit.HEART)
    assert len(candidates) == 1
    assert Card(CardSuit.HEART, CardRank.ACE) in candidates
