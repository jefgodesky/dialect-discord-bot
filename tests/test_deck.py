from unittest.mock import patch

from card.classes import Card
from deck.classes import Deck


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
