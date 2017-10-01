# -*- coding: utf-8 -*-
from enum import Enum, IntEnum, unique
from collections import namedtuple, defaultdict
import itertools
from copy import deepcopy
from operator import attrgetter


@unique
class CardSuit(Enum):
    SPADE = '♠'
    HEART = '♡'
    DIAMOND = '♢'
    CLUB = '♣'

    def __str__(self):
        return self.value


@unique
class CardRank(IntEnum):
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
        return '<{}({}{})>'.format(self.__class__.__name__, self.suit, self.rank)


@unique
class Player(Enum):
    NORTH = 'N'
    SOUTH = 'S'
    EAST = 'E'
    WEST = 'W'

    def next_player(self):
        next_player = {
            Player.NORTH: Player.EAST,
            Player.EAST: Player.SOUTH,
            Player.SOUTH: Player.WEST,
            Player.WEST: Player.NORTH
        }
        return next_player[self]


@unique
class Trump(Enum):
    NO_TRUMP = 'NT'
    SPADE = CardSuit.SPADE
    HEADT = CardSuit.HEART
    DIAMOND = CardSuit.DIAMOND
    CLUB = CardSuit.CLUB


class Hand:
    def __init__(self, cards=[]):
        self.cards = defaultdict(list)
        for card in cards:
            self.add_card(card)
        self.played = []

    def add_card(self, card):
        self.cards[card.suit].append(card)
        sorted(self.cards[card.suit], key=attrgetter('rank'))

    def candidate_cards(self, suit=None):
        if suit is not None and len(self.cards[suit]) > 0:
            return deepcopy(self.cards[suit])
        else:
            candidates = list(itertools.chain.from_iterable(self.cards.values()))
            return deepcopy(candidates)

    def play_card(self, card):
        self.cards[card.suit].remove(card)
        self.played.append(card)

    def reverse(self):
        self.add_card(self.played.pop())


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

            for suit, suit_cards in zip([CardSuit.SPADE, CardSuit.HEART, CardSuit.DIAMOND, CardSuit.CLUB], gib_hand.split('.')):
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
        self.trick = {}
        self.current_player = starting_player
        self.trump = trump
        self.winner = None

    def play_card(self, card):
        self.trick[self.current_player] = card

        if self.compare(card):
            self.winner = self.current_player

        self.current_player = self.current_player.next_player()

        if len(self.trick) == 4:
            return self.winner
        else:
            return None

    def compare(self, card):
        if self.winner is None:
            return True

        current_card = self.trick[self.winner]
        if card.suit == current_card.suit:
            return card.rank > current_card.rank
        elif card.suit == self.trump:
            return True
        else:
            return False


class GameState:
    def __init__(self, board, trump, starting_player, goal):
        self.board = board
        self.trump = trump
        self.next_player = starting_player
        self.current_trick = None
        self.ns_trick_count = 0
