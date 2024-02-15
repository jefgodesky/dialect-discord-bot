from typing import Literal

DeckType = Literal["voice", "age1", "age2", "age3", "legacy"]


class Deck:
    def __init__(self, deck_type: DeckType = "voice"):
        sizes = {"voice": 15, "age1": 22, "age2": 25, "age3": 14, "legacy": 6}
        self.deck_type = deck_type
        self.cards = [x + 1 for x in range(sizes[deck_type])]
