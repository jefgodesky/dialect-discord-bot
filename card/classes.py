from typing import Literal

DeckType = Literal["voice", "age1", "age2", "age3", "legacy"]


class Card:
    def __init__(self, deck_type: DeckType = "voice", index: int = 1):
        self.deck_type = deck_type
        self.index = index

    @property
    def filename(self):
        return self.deck_type + str(self.index).zfill(2) + ".png"
