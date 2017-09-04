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
    def __init__(self, cards=None):
        self.cards = defaultdict(list);
        for card in cards:
            self.add_card(card);
        self.played = []
        
    def add_card(self, card):
        self.cards[card.suit].append(card);
        sorted(self.cards[card.suit], key=attrgetter('rank'))
    
    def candidate_cards(self, suit=None):
        if suit is not None and len(self.cards[suit]) > 0:
            return deepcopy(self.cards[suit]);
        else:
            candidates = list(itertools.chain.from_iterable(self.cards.values()));
            return deepcopy(candidates);
    
    def play_card(self, card):
        self.cards[card.suit].remove(card);
        self.played.append(card);
    
    def reverse(self):
        self.add_card(self.played.pop());

class Board(namedtuple('Card', ['north', 'east', 'south', 'west'])):
    __slots__ = ()


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
