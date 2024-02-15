import random

from card.classes import Card, DeckType


class Deck:
    def __init__(self, deck_type: DeckType = "voice"):
        sizes = {"voice": 15, "age1": 22, "age2": 25, "age3": 14, "legacy": 6}
        self.deck_type = deck_type
        self.cards = [Card(deck_type, x + 1) for x in range(sizes[deck_type])]

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()
