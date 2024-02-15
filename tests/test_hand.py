from unittest.mock import patch, mock_open

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
