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
