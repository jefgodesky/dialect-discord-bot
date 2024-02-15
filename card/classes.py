from deck.classes import DeckType


class Card:
    def __init__(self, deck_type: DeckType = "voice", index: int = 1):
        self.deck_type = deck_type
        self.index = index
