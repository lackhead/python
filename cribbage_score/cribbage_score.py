'''
   Cribbage Scoring

   DESCRIPTION:
   Cribbage is a game played with a standard deck of 52
    cards. There are several phases or rounds to playing cribbage: deal,
    discard, play and show. Players can earn points during the play and show
    rounds. This challenge is specific to the show phase of gameplay only.
    Each player's hand consists of 4 cards and an additional face up card.
    During the show round, each player scores points based on the content in
    their hand (plus the face up card). Points are awarded for the
    following:
        Any number of cards that add up to 15 (regardless of
            suit) – 2 points
        Runs of 3, 4, or 5 cards – 3, 4 and 5 points respectively
        Pairs: 2, 3, or 4 of a kind – 2, 6 and 12 points
            respectively
        Flushes: 4 or 5 cards of the same suit (note, the
            additional face up card is not counted for a 4 card flush) – 4
            and 5 points respectively
        Nobs: A Jack of the same suit as the additional face up card – 1
            point
    Note: cards can be used more than once, for each combo
'''

from itertools import combinations

# the sorted lists of suits and ranks
suits = list('DCHS')
ranks = [str(n) for n in range(2, 11)] + list('JQKA')


# Two functions for sorting groups of cards
def byrank(c):
    return c.rank


def bysuit(c):
    return c.suit


def isRun(cards):
    '''
    given a list of cards, do they run in rank order?
    '''
    # Is the null list a run?
    if not cards:
        return False

    # don't assume they are sorted
    sortedCards = sorted(cards, key=lambda x: x.rank)

    # run through the list
    i = ranks.index(sortedCards[0].rank)
    for x in sortedCards[1:]:
        j = ranks.index(x.rank)
        if j != i + 1:
            return False
        i = j
    return True


def isFifteen(cards):
    '''
    Given a list of cards, do they sum to 15?
    '''
    s = 0
    for r in [x.rank for x in cards]:
        if r == "A":
            s += 1
        elif r in "JQK":
            s += 10
        else:
            s += int(r)
    return (s == 15)


class Card(object):
    '''
    This simple class represents a card that has a suit and a rank.
    '''
    def __init__(self, str):
        # str is a string of rank/suit
        str = str.upper()
        self.__rank = str[:-1]
        self.__suit = str[-1:]
        # make sure it is well formed
        if self.__rank not in ranks:
            raise ValueError("{} is not a valid rank".format(self.__rank))
        if self.__suit not in suits:
            raise ValueError("{} is not a valid suit".format(self.__rank))

    @property
    def rank(self):
        return self.__rank

    @property
    def suit(self):
        return self.__suit

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, self.rank, self.suit)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.rank == other.rank and self.suit == other.suit
        return False

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit

    def __lt__(self, other):
        if self.rank == other.rank:
            return (suits.index(self.suit) < suits.index(other.suit))
        else:
            return (ranks.index(self.rank) < ranks.index(other.rank))

    def __hash__(self):
        return hash(repr(self))

    def __str__(self):
        return self.rank + self.suit


class CribbageHand(object):
    '''
    This class contains a cribbage hand, which is 4 in-hand cards a crib
    card. The important method is score_hand() which returns the score
    plus the constituents of the score.
    '''

    def __init__(self, crib, *cards):
        self.__crib = Card(crib)
        # convert through set to make cards unique
        s = set(Card(x) for x in cards)
        if self.__crib in s:
            raise ValueError("Crib duplicated in hand.")
        if len(s) != 4:
            raise ValueError("Inappropriate hand: {}".format(s))
        self.__hand = sorted(list(s))

    @property
    def crib(self):
        return self.__crib

    @property
    def hand(self):
        return self.__hand

    @property
    def cards(self):
        return [self.crib] + self.hand

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, self.crib, self.hand)

    @property
    def pairs(self):
        '''
        This returns a list of all the pairs (by rank) in the hand
        '''
        return sorted([(x, y) for x, y in combinations(self.cards, 2)
            if x != y and x.rank == y.rank])

    @property
    def runs(self):
        '''
        This returns a list of all the runs of length 3,4,5 in the hand
        '''
        # in order not to return subsets of runs, start big
        if isRun(self.cards):
            return [sorted(self.cards, key=byrank)]
        # next try 4's
        runs = [sorted(p, key=byrank) for p in combinations(self.cards, 4)
                if isRun(p)]
        if runs:
            return runs
        # only thing left are 3's
        return [sorted(p, key=byrank) for p in combinations(self.cards, 3)
                if isRun(p)]

    @property
    def flush(self):
        '''
        This tests to see if the hand is a flush. Note that there are only
        two possibilities: a flush in the hand, or a flush in the hand with
        a matching crib.
        '''
        flush = [x for x in self.hand if (x.suit == self.hand[0].suit)]
        if len(flush) == 4:
            if self.crib.suit == flush[0].suit:
                flush.append(self.crib)
            return flush
        return []

    @property
    def nobs(self):
        '''
        His Nobs is when the hand contains the jack of the same suit as the
        crib
        '''
        s = self.crib.suit
        for x in self.hand:
            if x.suit == s and x.rank == "J":
                return x
        return False

    @property
    def fifteens(self):
        '''
        All combinations of cards that sum to 15
        '''
        f = []
        for size in range(2, len(self.cards)):
            f += [x for x in combinations(self.cards, size) if isFifteen(x)]
        return f

    @property
    def score(self):
        '''
        Sum up everything we've got
        '''
        sum = 2 * len(self.pairs)
        for r in self.runs:
            sum += len(r)
        sum += len(self.flush)
        sum += 2 * len(self.fifteens)
        if self.nobs:
            sum += 1
        return sum

    @property
    def scores(self):
        '''
        return a dictionary containing all the scores
        '''
        return {
                "pairs": self.pairs,
                "runs": self.runs,
                "flush": self.flush,
                "fifteens": self.fifteens,
                "nobs": self.nobs,
                "score": self.score
        }
