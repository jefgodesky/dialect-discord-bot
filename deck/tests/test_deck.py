from ..deck import Deck


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
