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

    # function play_card
    hand.play_card(HA)
    candidates = hand.candidate_cards(CardSuit.HEART)
    assert HA not in candidates
    assert len(candidates) == 3

    # function step_back
    hand.step_back()
    candidates = hand.candidate_cards(CardSuit.HEART)
    assert len(candidates) == 1
    assert HA in candidates


def test_Hand_empty():
    hand = Hand()
    candidates = hand.candidate_cards()
    assert len(candidates) == 0

    with pytest.raises(ValueError):
        hand.play_card(Card(CardSuit.SPADE, CardRank.ACE))

    with pytest.raises(IndexError):
        hand.step_back()


@pytest.mark.xfail
def test_Hand_duplicate_card():
    with pytest.raises(ValueError):
        SA = Card(CardSuit.SPADE, CardRank.ACE)
        hand = Hand(cards=[SA, SA])


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
