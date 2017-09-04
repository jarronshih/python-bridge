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

def test_Hand():
    hand = Hand(cards=[Card(CardSuit.SPADE, CardRank.ACE), 
                       Card(CardSuit.HEART, CardRank.ACE), 
                       Card(CardSuit.DIAMOND, CardRank.ACE),
                       Card(CardSuit.SPADE, CardRank.KING)]);
    
    card = hand.play_card(4);
    assert card is None;
    
    card = hand.play_card(2, CardSuit.SPADE);
    assert card is None;
    
    card = hand.play_card(1, CardSuit.DIAMOND);
    assert card is None;
    
    card = hand.play_card(2)
    assert card == Card(CardSuit.HEART, CardRank.ACE);
    card = hand.play_card(1, CardSuit.SPADE);
    assert card == Card(CardSuit.SPADE, CardRank.KING);
    card = hand.play_card(0, CardSuit.CLUB);
    assert card == Card(CardSuit.SPADE, CardRank.ACE);
    
    assert len(hand.cards[CardSuit.SPADE]) == 0;
    hand.reverse();
    assert len(hand.cards[CardSuit.SPADE]) == 1;
    hand.reverse();
    assert len(hand.cards[CardSuit.SPADE]) == 2;
    assert (hand.cards[CardSuit.SPADE])[0].rank == CardRank.ACE;
    
    assert len(hand.cards[CardSuit.HEART]) == 0;
    hand.reverse();
    assert len(hand.cards[CardSuit.HEART]) == 1;