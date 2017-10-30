# Test suite for cribbage_score.py

from collections import Counter
from cribbage_score import Card, CribbageHand
import pytest


# Class with tests in them
class TestCard(object):
    '''
    Tests for the Card class
    '''

    # The following tests also hit the rank/suit properties
    def test_card_creation(self):
        c = Card("2S")
        assert c.rank == "2"
        assert c.suit == "S"

    def test_card_creation_ten(self):
        c = Card("10C")
        assert c.rank == "10"
        assert c.suit == "C"

    def test_card_creation_case(self):
        c = Card("jd")
        assert c.rank == "J"
        assert c.suit == "D"

    def test_card_creation_facecard(self):
        c = Card("QH")
        assert c.rank == "Q"
        assert c.suit == "H"

    def test_card_creation_badrank(self):
        with pytest.raises(ValueError):
            Card("11S")

    def test_card_creation_badsuit(self):
        with pytest.raises(ValueError):
            Card("5L")

    def test_card_repr(self):
        c = Card("7D")
        assert repr(c) == "Card('7', 'D')"

    def test_card_eq(self):
        c = Card("3S")
        assert c == Card("3s")

    def test_card_ne(self):
        c = Card("AC")
        assert c != Card("AH")

    def test_card_order(self):
        c1 = Card("4S")
        c2 = Card("5C")
        c3 = Card("5H")
        assert c1 < c2
        assert c2 < c3

    def test_card_str(self):
        c = Card("4C")
        assert str(c) == "4C"


class TestCribbageHand(object):
    '''
    Tests for the CribbageHand class
    '''

    def test_cribhand_creation(self):
        ch = CribbageHand("AS", "3D", "7H", "QS", "3C")
        assert ch.crib == Card("AS")
        assert Card('QS') in ch.hand
        assert Counter(ch.cards) == \
            Counter([Card(x) for x in ["AS", "3D", "7H", "QS", "3C"]])

    def test_cribhand_args(self):
        with pytest.raises(ValueError):
            ch = CribbageHand("AS", "AS", "7H", "QS", "3C")
        with pytest.raises(ValueError):
            ch = CribbageHand("AS", "7H", "QS", "3C")

    def test_cribhand_repr(self):
        ch = CribbageHand("AS", "AC", "7H", "QS", "3C")
        assert repr(ch) == "CribbageHand(Card('A', 'S'), [Card('3', 'C'), Card('7', 'H'), Card('Q', 'S'), Card('A', 'C')])"

    def test_cribhand_pairs(self):
        ch = CribbageHand("AS", "AC", "7H", "QS", "3C")
        assert Counter(ch.pairs) == Counter([(Card("AS"), Card("AC"))])
        ch = CribbageHand("AS", "AC", "AH", "QS", "AD")
        assert len(ch.pairs) == 6
        ch = CribbageHand("AS", "KC", "QH", "2S", "3D")
        assert len(ch.pairs) == 0

    def test_cribhand_runs(self):
        ch = CribbageHand("3S", "4C", "7H", "6S", "5C")
        assert len(ch.runs) == 1
        ch = CribbageHand("7S", "8C", "8H", "9S", "9D")
        assert len(ch.runs) == 4
        ch = CribbageHand("AS", "KC", "9H", "4S", "3D")
        assert len(ch.runs) == 0

    def test_cribhand_flush(self):
        ch = CribbageHand("3S", "4C", "7C", "JC", "5C")
        assert len(ch.flush) == 4
        ch = CribbageHand("3C", "4S", "7C", "JC", "5C")
        assert len(ch.flush) == 0
        ch = CribbageHand("JS", "4S", "7S", "QS", "5S")
        assert len(ch.flush) == 5

    def test_cribhand_nobs(self):
        ch = CribbageHand("3S", "4C", "7H", "JS", "5C")
        assert ch.nobs == Card("JS")
        ch = CribbageHand("JS", "4C", "7H", "JH", "5C")
        assert ch.nobs == False

    def test_cribhand_fifteens(self):
        ch = CribbageHand("3S", "4C", "7H", "JS", "5C")
        assert len(ch.fifteens) == 2
        ch = CribbageHand("JS", "4C", "6H", "JH", "2C")
        assert len(ch.fifteens) == 0
        ch = CribbageHand("10S", "7C", "7H", "8S", "5C")
        assert len(ch.fifteens) == 3
        ch = CribbageHand("10S", "KC", "JH", "5S", "5C")
        assert len(ch.fifteens) == 6

    def test_cribhand_score(self):
        ch = CribbageHand("3S", "4C", "7H", "JS", "5C")
        assert ch.score == 8
        ch = CribbageHand("JS", "4C", "6H", "JH", "2C")
        assert ch.score == 2
        ch = CribbageHand("10H", "7H", "8H", "9H", "5C")
        assert ch.score == 7
        ch = CribbageHand("10H", "7H", "8H", "JH", "5C")
        assert ch.score == 7
        ch = CribbageHand("3S", "4C", "7H", "JH", "QC")
        assert ch.score == 0
        ch = CribbageHand("10D", "JD", "JH", "10C", "QC")
        assert ch.score == 17
