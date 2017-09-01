# -*- coding: utf-8 -*-
from enum import Enum, unique, auto
from collections import namedtuple


@unique
class CardSuit(Enum):
    SPADE = '♠'
    HEART = '♡'
    DIAMOND = '♢'
    CLUB = '♣'

    def __str__(self):
        return self.value


@unique
class CardRank(Enum):
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

    @classmethod
    def next_player(cls, player):
        next_player = {
            cls.NORTH: cls.EAST,
            cls.EAST: cls.SOUTH,
            cls.SOUTH: cls.WEST,
            cls.WEST: cls.NORTH
        }
        return next_player[player]


@unique
class Trump(Enum):
    NO_TRUMP = auto()
    SPADE = auto()
    HEADT = auto()
    DIAMOND = auto()
    CLUB = auto()


class Hand:
    def __init__(self, cards=None):
        self.cards = cards


class Board(namedtuple('Card', ['north', 'east', 'south', 'west'])):
    __slots__ = ()


class Trick:
    def __init__(self):
        self.trick = []

    def set_trump(self, suit):
        pass

    def play_card(self, card):
        pass


class GameState:
    def __init__(self, board, trump, starting_player, goal):
        self.board = board
        self.trump = trump
        self.next_player = starting_player
        self.current_trick = None
        self.ns_trick_count = 0
