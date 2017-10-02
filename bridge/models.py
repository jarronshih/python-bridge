# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, unique
from collections import namedtuple, defaultdict
import itertools
from copy import deepcopy
from operator import attrgetter


@unique
class CardSuit(Enum):
    __order__ = 'SPADE HEART DIAMOND CLUB'
    SPADE = '♠'
    HEART = '♥'
    DIAMOND = '♦'
    CLUB = '♣'

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if other.__class__ in [CardSuit, Trump]:
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other):
        if other.__class__ in [CardSuit, Trump]:
            return self.value != other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)


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
        return '<{}{}>'.format(self.__class__.__name__, self.suit, self.rank)

    def __str__(self):
        return '{}{}'.format(self.suit, self.rank)


@unique
class Player(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.value)

    def next_player(self):
        next_player = {
            Player.NORTH: Player.EAST,
            Player.EAST: Player.SOUTH,
            Player.SOUTH: Player.WEST,
            Player.WEST: Player.NORTH
        }
        return next_player[self]

    def previous_player(self):
        next_player = {
            Player.NORTH: Player.WEST,
            Player.EAST: Player.NORTH,
            Player.SOUTH: Player.EAST,
            Player.WEST: Player.SOUTH
        }
        return next_player[self]


@unique
class Trump(Enum):
    __order__ = 'NO_TRUMP SPADE HEART DIAMOND CLUB'
    NO_TRUMP = 'NT'
    SPADE = CardSuit.SPADE.value
    HEART = CardSuit.HEART.value
    DIAMOND = CardSuit.DIAMOND.value
    CLUB = CardSuit.CLUB.value

    def __repr__(self):
        return '<{}:{}>'.format(self.__class__.__name__, self.value)

    def __eq__(self, other):
        if other.__class__ in [CardSuit, Trump]:
            return self.value == other.value
        return NotImplemented

    def __ne__(self, other):
        if other.__class__ in [CardSuit, Trump]:
            return self.value != other.value
        return NotImplemented

    def __hash__(self):
        return hash(self.value)


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
        sorted(self.cards[card.suit], key=attrgetter('rank'))

    def candidate_cards(self, suit=None):
        if suit is not None and len(self.cards[suit]) > 0:
            yield from deepcopy(self.cards[suit])
        else:
            candidates = list(itertools.chain.from_iterable(self.cards.values()))
            yield from deepcopy(candidates)

    def play_card(self, card):
        self.cards[card.suit].remove(card)
        self.played.append(card)


class Board(namedtuple('Board', ['north', 'east', 'south', 'west'])):
    __slots__ = ()

    def get_hand(self, player):
        player_hands = {
            Player.NORTH: self.north,
            Player.SOUTH: self.south,
            Player.EAST: self.east,
            Player.WEST: self.west
        }
        if player in player_hands:
            return player_hands[player]

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
