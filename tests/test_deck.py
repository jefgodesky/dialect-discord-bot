from unittest.mock import patch, mock_open, MagicMock

from discord import Member

from card.classes import Card
from cardlist.classes import CardList
from player.classes import Player
from deck.classes import Deck


class TestDeck:
    def test_creates_deck(self):
        deck = Deck()
        assert isinstance(deck, Deck)

    @patch("cardlist.classes.open", new_callable=mock_open, read_data="data")
    def test_pass_labels(self, open_mock):
        card_list = CardList()
        assert open_mock.call_count == 1
        Deck(card_list=card_list)
        assert open_mock.call_count == 1

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

    def test_labels(self):
        deck = Deck("voice")
        assert deck.get_label(1) == "Explorer"

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
        players = [Player(MagicMock(spec=Member)) for _ in range(3)]
        deck = Deck("voice")
        deck.deal(3, players)
        assert len(deck.cards) == 6
        assert all(len(player.cards) == 3 for player in players)
