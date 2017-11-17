import re
import functools

DIRECTION = ['S', 'W', 'N', 'E']


class Suit(object):
    CARD_NUMBER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

    def __init__(self, suit):
        self.suit = suit

    def __str__(self):
        ret = ''
        for k in self.CARD_NUMBER:
            if k in self.suit:
                ret += k
        return ret


class Player(object):
    def __init__(self, hand):
        self.hand = hand

        def suit_parser(hand, reg):
            cards = re.match(reg, hand)
            if cards:
                return cards.group(1)
            else:
                return ''

        self._spades = Suit(suit_parser(hand, r'.*S(.*)H.*'))
        self._hearts = Suit(suit_parser(hand, r'.*H(.*)D.*'))
        self._diams = Suit(suit_parser(hand, r'.*D(.*)C.*'))
        self._clubs = Suit(suit_parser(hand, r'.*C(.*)$'))

    @classmethod
    def build_from_others(cls, others):
        spades = ''
        for c in Suit.CARD_NUMBER:
            for p in others:
                if c in p._spades.suit:
                    break;
            else:
                spades += c

        hearts = ''
        for c in Suit.CARD_NUMBER:
            for p in others:
                if c in p._hearts.suit:
                    break;
            else:
                hearts += c

        diams = ''
        for c in Suit.CARD_NUMBER:
            for p in others:
                if c in p._diams.suit:
                    break;
            else:
                diams += c

        clubs = ''
        for c in Suit.CARD_NUMBER:
            for p in others:
                if c in p._clubs.suit:
                    break;
            else:
                clubs += c

        player = Player('')
        player._spades = Suit(spades)
        player._hearts = Suit(hearts)
        player._diams = Suit(diams)
        player._clubs = Suit(clubs)

        return player



    @property
    def spades(self):
        return str(self._spades)

    @property
    def hearts(self):
        return str(self._hearts)

    @property
    def diams(self):
        return str(self._diams)

    @property
    def clubs(self):
        return str(self._clubs)


class LinFormat(object):
    """https://github.com/morgoth/lin"""
    deck = ["SA", "SK", "SQ", "SJ", "ST", "S9", "S8", "S7", "S6", "S5", "S4", "S3", "S2",
            "HA", "HK", "HQ", "HJ", "HT", "H9", "H8", "H7", "H6", "H5", "H4", "H3", "H2",
            "DA", "DK", "DQ", "DJ", "DT", "D9", "D8", "D7", "D6", "D5", "D4", "D3", "D2",
            "CA", "CK", "CQ", "CJ", "CT", "C9", "C8", "C7", "C6", "C5", "C4", "C3", "C2"]

    def __init__(self, lin):
        super().__init__()
        self._lin = lin

    def __str__(self):
        # return self.lin
        return '{lin.board_name}[{lin.dealer}] N({lin.north_name}): S({lin.south_name}): {lin.south_hand} E({lin.east_name}): W({lin.west_name}):'.format(lin=self)

    def get_tag_value(self, tag):
        regex = re.escape(tag) + r"\|(.*?)\|"
        res = re.findall(regex, self._lin)
        if res:
            return res[0]
        else:
            return None

    @property
    def data(self):
        return self._lin

    @property
    @functools.lru_cache()
    def south_name(self):
        pn = self.get_tag_value('pn')
        return pn.split(',')[0]

    @property
    @functools.lru_cache()
    def west_name(self):
        pn = self.get_tag_value('pn')
        return pn.split(',')[1]

    @property
    @functools.lru_cache()
    def north_name(self):
        pn = self.get_tag_value('pn')
        return pn.split(',')[2]

    @property
    @functools.lru_cache()
    def east_name(self):
        pn = self.get_tag_value('pn')
        return pn.split(',')[3]

    @property
    @functools.lru_cache()
    def dealer(self):
        direction = ['S', 'W', 'N', 'E']
        dealer = self.get_tag_value('md')[0]
        return direction[int(dealer) - 1]

    @property
    @functools.lru_cache()
    def south(self):
        hand = self.get_tag_value('md').split(',')[0][1:]
        return Player(hand)

    @property
    @functools.lru_cache()
    def west(self):
        hand = self.get_tag_value('md').split(',')[1]
        return Player(hand)

    @property
    @functools.lru_cache()
    def north(self):
        hand = self.get_tag_value('md').split(',')[2]
        return Player(hand)

    @property
    @functools.lru_cache()
    def east(self):
        return Player.build_from_others([self.south, self.west, self.north])

    @property
    @functools.lru_cache()
    def board_number(self):
        return self.get_tag_value('ah').replace('Board ', '')

    @property
    @functools.lru_cache()
    def bids(self):
        pass

    @property
    @functools.lru_cache()
    def cards(self):
        pass

    @property
    @functools.lru_cache()
    def claim(self):
        pass

    @property
    @functools.lru_cache()
    def vulnerable(self):
        pass


'''
pn|natsuki,shuan,chengwu2,wkc|st||md|4S3TKH238AD35C249T,S78AH7JKD2489QKCQ,S259H459QDJAC3567,|rh||ah|Board 18|sv|n|mb|p|mb|p|mb|1D|mb|p|mb|1S|mb|p|mb|2S|mb|p|mb|3S|mb|p|mb|4S|mb|p|mb|p|mb|p|pc|C4|pc|CQ|pc|C3|pc|C8|pc|S7|pc|S2|pc|SQ|pc|SK|pc|H3|pc|H7|pc|HQ|pc|H6|pc|H5|pc|HT|pc|HA|pc|HJ|pc|D5|pc|DK|pc|DA|pc|D6|pc|H4|pc|D7|pc|H2|pc|HK|pc|SA|pc|S5|pc|S4|pc|S3|pc|S8|pc|S9|pc|SJ|pc|ST|mc|9|
'''
