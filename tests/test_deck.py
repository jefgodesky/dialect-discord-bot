from unittest.mock import patch

from card.classes import Card
from hand.classes import Hand
from deck.classes import Deck, DeckLabels


class TestDeck:
    def test_creates_deck(self):
        deck = Deck()
        assert isinstance(deck, Deck)

    def test_creates_voice_deck(self):
        deck = Deck("voice")
        assert deck.deck_type == "voice"

    def test_creates_legacy_deck(self):
        deck = Deck("legacy")
        assert deck.deck_type == "legacy"

    def test_creates_age1_deck(self):
        deck = Deck("age1")
        assert deck.deck_type == "age1"

    def test_creates_age2_deck(self):
        deck = Deck("age2")
        assert deck.deck_type == "age2"

    def test_creates_age3_deck(self):
        deck = Deck("age3")
        assert deck.deck_type == "age3"

    def test_voice_has_15_cards(self):
        deck = Deck("voice")
        assert len(deck.cards) == 15

    def test_legacy_has_6_cards(self):
        deck = Deck("legacy")
        assert len(deck.cards) == 6

    def test_age1_has_22_cards(self):
        deck = Deck("age1")
        assert len(deck.cards) == 22

    def test_age2_has_25_cards(self):
        deck = Deck("age2")
        assert len(deck.cards) == 25

    def test_age3_has_14_cards(self):
        deck = Deck("age3")
        assert len(deck.cards) == 14

    def test_voice_has_voice_cards(self):
        deck = Deck("voice")
        for card in deck.cards:
            assert card.deck_type == "voice"

    def test_age1_has_age1_cards(self):
        deck = Deck("age1")
        for card in deck.cards:
            assert card.deck_type == "age1"

    def test_age2_has_age2_cards(self):
        deck = Deck("age2")
        for card in deck.cards:
            assert card.deck_type == "age2"

    def test_age3_has_age3_cards(self):
        deck = Deck("age3")
        for card in deck.cards:
            assert card.deck_type == "age3"

    def test_legacy_has_legacy_cards(self):
        deck = Deck("legacy")
        for card in deck.cards:
            assert card.deck_type == "legacy"

    def test_shuffle(self):
        deck = Deck("legacy")
        with patch("random.shuffle") as mock_shuffle:
            deck.shuffle()
            mock_shuffle.assert_called_once_with(deck.cards)

    def test_draw_returns_card(self):
        deck = Deck("legacy")
        card = deck.draw()
        assert isinstance(card, Card)

    def test_draw_removes_card(self):
        deck = Deck("legacy")
        card = deck.draw()
        assert len(deck.cards) == 5
        for c in deck.cards:
            assert card.index != c.index

    def test_deal(self):
        h1 = Hand()
        h2 = Hand()
        h3 = Hand()

        deck = Deck("voice")
        deck.deal(3, [h1, h2, h3])

        assert len(deck.cards) == 6
        assert len(h1.cards) == 3
        assert len(h2.cards) == 3
        assert len(h3.cards) == 3


class TestDeckLabels:
    def test_creates_deck_labels(self):
        labels = DeckLabels()
        assert isinstance(labels, DeckLabels)

    def test_loads_labels(self):
        labels = DeckLabels()
        assert labels.get("voice", 1) == "Explorer"
