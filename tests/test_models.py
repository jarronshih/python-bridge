import pytest
from bridge.models import Trick, Trump, Player, Card, CardSuit, CardRank, Hand, Board


def test_trick():
    trick = Trick(trump=Trump.NO_TRUMP, starting_player=Player.EAST)

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.KING))
    assert t is None

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.TWO))
    assert t is None

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.ACE))
    assert t is None

    t = trick.play_card(Card(CardSuit.SPADE, CardRank.THREE))
    assert t is Player.WEST

    card = trick.step_back()
    assert card == Card(CardSuit.SPADE, CardRank.THREE)

    card = trick.step_back()
    assert card == Card(CardSuit.SPADE, CardRank.ACE)

    t = trick.play_card(Card(CardSuit.HEART, CardRank.ACE))
    assert t is None

    t = trick.play_card(Card(CardSuit.HEART, CardRank.KING))
    assert t is Player.EAST


def test_Hand():
    SA = Card(CardSuit.SPADE, CardRank.ACE)
    SK = Card(CardSuit.SPADE, CardRank.KING)
    HA = Card(CardSuit.HEART, CardRank.ACE)
    DA = Card(CardSuit.DIAMOND, CardRank.ACE)
    hand = Hand(cards=[SA, SK, HA, DA])

    # function candidate_cards
    assert len(list(hand.candidate_cards())) == 4
    assert len(list(hand.candidate_cards(CardSuit.SPADE))) == 2
    assert len(list(hand.candidate_cards(CardSuit.HEART))) == 1
    assert len(list(hand.candidate_cards(CardSuit.DIAMOND))) == 1
    assert len(list(hand.candidate_cards(CardSuit.CLUB))) == 4

    # function play_card
    hand.play_card(HA)
    assert HA not in list(hand.candidate_cards(CardSuit.HEART))
    assert len(list(hand.candidate_cards(CardSuit.HEART))) == 3


def test_Hand_empty():
    hand = Hand()
    assert len(list(hand.candidate_cards())) == 0

    with pytest.raises(ValueError):
        hand.play_card(Card(CardSuit.SPADE, CardRank.ACE))


@pytest.mark.xfail
def test_Hand_duplicate_card():
    with pytest.raises(ValueError):
        SA = Card(CardSuit.SPADE, CardRank.ACE)
        Hand(cards=[SA, SA])


def test_Trump_eq_CardSuit():
    assert Trump.NO_TRUMP != CardSuit.SPADE
    assert Trump.SPADE == CardSuit.SPADE
    assert Trump.HEART == CardSuit.HEART
    assert Trump.DIAMOND == CardSuit.DIAMOND
    assert Trump.CLUB == CardSuit.CLUB
    assert CardSuit.SPADE != Trump.NO_TRUMP
    assert CardSuit.SPADE == Trump.SPADE
    assert CardSuit.HEART == Trump.HEART
    assert CardSuit.DIAMOND == Trump.DIAMOND
    assert CardSuit.CLUB == Trump.CLUB


def test_Board():
    SA = Card(CardSuit.SPADE, CardRank.ACE)
    SK = Card(CardSuit.SPADE, CardRank.KING)
    HA = Card(CardSuit.HEART, CardRank.ACE)
    DA = Card(CardSuit.DIAMOND, CardRank.ACE)
    north = Hand([SA])
    south = Hand([SK])
    east = Hand([HA])
    west = Hand([DA])

    board = Board(north=north, south=south, east=east, west=west)
    assert north == board.get_hand(Player.NORTH)
    assert south == board.get_hand(Player.SOUTH)
    assert east == board.get_hand(Player.EAST)
    assert west == board.get_hand(Player.WEST)
