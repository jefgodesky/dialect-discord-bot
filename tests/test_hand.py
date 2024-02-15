from card.classes import Card
from hand.classes import Hand


class TestHand:
    def test_creates_hand(self):
        hand = Hand()
        assert isinstance(hand, Hand)

    def test_draw_adds_card(self):
        card = Card("voice", 1)
        hand = Hand()
        hand.draw(card)
        assert len(hand.cards) == 1
        assert hand.cards[0] == card
