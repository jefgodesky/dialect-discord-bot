from unittest.mock import patch, mock_open

import pytest

from card.classes import Card
from cardlist.classes import CardList
from hand.classes import Hand


class TestHand:
    def test_creates_hand(self):
        hand = Hand()
        assert isinstance(hand, Hand)

    @patch("cardlist.classes.open", new_callable=mock_open, read_data="data")
    def test_pass_labels(self, open_mock):
        card_list = CardList()
        assert open_mock.call_count == 1
        Hand(card_list=card_list)
        assert open_mock.call_count == 1

    def test_draw_adds_card(self):
        card = Card("voice", 1)
        hand = Hand()
        hand.draw(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card

    @pytest.fixture
    def draw_cards(self):
        hand = Hand()
        [hand.draw(Card("voice", x + 1)) for x in range(3)]
        return hand

    def test_play_removes_card(self, draw_cards):
        draw_cards.play("Explorer")
        assert len(draw_cards.cards) == 2

    def test_plays_specified_card(self, draw_cards):
        played = draw_cards.play("Ruler")
        assert played.deck_type == "voice"
        assert played.index == 2
        assert played.label == "Ruler"

    def test_cant_play_what_you_dont_have(self, draw_cards):
        played = draw_cards.play("Celebrity")
        assert played is None
