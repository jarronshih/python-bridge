# -*- coding: utf-8 -*-
from enum import IntEnum, unique
from collections import namedtuple, defaultdict
from operator import attrgetter


@unique
class CardSuit(IntEnum):
    __order__ = 'SPADE HEART DIAMOND CLUB'

    SPADE = 3
    HEART = 2
    DIAMOND = 1
    CLUB = 0

    def __str__(self):
        return self.value


@unique
class CardRank(IntEnum):
    __order__ = 'ACE KING QUEEN JACK TEN NINE EIGHT SEVEN SIX FIVE FOUR THREE TWO'

    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2

    def __str__(self):
        rank_map = {
            self.ACE: 'A',
            self.KING: 'K',
            self.QUEEN: 'Q',
            self.JACK: 'J',
            self.TEN: 'T'
        }
        try:
            return rank_map[self]
        except KeyError:
            return str(self.value)

    @classmethod
    def string_to_rank(cls, card_string):
        rank_map = {
            'A': CardRank.ACE,
            'K': CardRank.KING,
            'Q': CardRank.QUEEN,
            'J': CardRank.JACK,
            'T': CardRank.TEN,
            '9': CardRank.NINE,
            '8': CardRank.EIGHT,
            '7': CardRank.SEVEN,
            '6': CardRank.SIX,
            '5': CardRank.FIVE,
            '4': CardRank.FOUR,
            '3': CardRank.THREE,
            '2': CardRank.TWO
        }
        return rank_map[card_string.upper()]


class Card(namedtuple('Card', ['suit', 'rank'])):
    __slot__ = ()

    def __repr__(self):
        return '<{}>'.format(self.__str__())

    def __str__(self):
        return '{}{}'.format(self.suit, self.rank)


@unique
class Player(IntEnum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.value)

    def next_player(self):
        return self._next_player_map[self]

    def previous_player(self):
        return self._previous_player_map[self]


Player._next_player_map = {
    Player.NORTH: Player.EAST,
    Player.EAST: Player.SOUTH,
    Player.SOUTH: Player.WEST,
    Player.WEST: Player.NORTH
}

Player._previous_player_map = {
    Player.NORTH: Player.WEST,
    Player.EAST: Player.NORTH,
    Player.SOUTH: Player.EAST,
    Player.WEST: Player.SOUTH
}


@unique
class Trump(IntEnum):
    __order__ = 'NO_TRUMP SPADE HEART DIAMOND CLUB'

    NO_TRUMP = 4
    SPADE = 3
    HEART = 2
    DIAMOND = 1
    CLUB = 0

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.value)


class Hand:
    def __init__(self, cards=[]):
        self.cards = defaultdict(list)
        for card in cards:
            self.add_card(card)
        self.played = []

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.__str__())

    def __str__(self):
        ret = []
        for suit in CardSuit:

            if len(self.cards[suit]) == 0:
                ret.append('{}-'.format(suit.value))
            else:
                ret.append('{}{}'.format(suit.value, ''.join(map(lambda c: str(c.rank), self.cards[suit]))))

        return ' '.join(ret)

    def add_card(self, card):
        self.cards[card.suit].append(card)
        self.cards[card.suit].sort(key=attrgetter('rank'))

    def candidate_cards(self, suit=None):

        def suit_gen(suit_cards):
            suit_len = len(suit_cards)
            for i in range(suit_len):
                yield suit_cards[i]

        if suit is not None and len(self.cards[suit]) > 0:
            yield from suit_gen(self.cards[suit])
        else:
            for suit in CardSuit:
                if self.cards:
                    yield from suit_gen(self.cards[suit])

    def play_card(self, card):
        self.cards[card.suit].remove(card)
        self.played.append(card)


class Board(namedtuple('Board', ['north', 'east', 'south', 'west'])):
    __slots__ = ()

    def get_hand(self, player):
        return getattr(self, player.name.lower())

    @classmethod
    def create_from_gib(cls, gib_string):
        """
        W N E S
        """
        def gib_to_hand(gib_hand):
            cards = []

            for suit, suit_cards in zip(CardSuit, gib_hand.split('.')):
                for card in suit_cards:
                    cards.append(Card(suit=suit, rank=CardRank.string_to_rank(card)))

            return Hand(cards)

        gib_hands = gib_string.split(' ')
        return Board(
            west=gib_to_hand(gib_hands[0]),
            north=gib_to_hand(gib_hands[1]),
            east=gib_to_hand(gib_hands[2]),
            south=gib_to_hand(gib_hands[3])
        )


class Trick:
    def __init__(self, trump, starting_player):
        self.trick = []
        self.starting_player = starting_player
        self.trump = trump

    def play_card(self, card):
        self.trick.append(card)

        if len(self.trick) == 4:
            win_card = None
            winner = None
            current_player = self.starting_player
            for card in self.trick:
                win_card, winner = self.compare(win_card, winner, card, current_player)
                current_player = current_player.next_player()
            return winner
        else:
            return None

    def compare(self, win_card, winner, card, player):
        if win_card is None:
            return card, player

        if card.suit == win_card.suit:
            if card.rank > win_card.rank:
                return card, player
            else:
                return win_card, winner
        elif card.suit == self.trump:
            return card, player
        else:
            return win_card, winner

    def trick_suit(self):
        if len(self.trick) == 0:
            return None
        else:
            return self.trick[0].suit

    def step_back(self):
        if len(self.trick) == 0:
            return None
        else:
            return self.trick.pop()
