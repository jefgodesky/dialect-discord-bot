from card.classes import Card


class Hand:
    def __init__(self):
        self.cards = []

    def draw(self, card: Card) -> None:
        self.cards.append(card)
