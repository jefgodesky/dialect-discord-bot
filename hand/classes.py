from card.classes import Card
from cardlist.classes import CardList


class Hand:
    def __init__(self, card_list: CardList = CardList()):
        self.cards = []
        self.card_list = card_list

    def draw(self, card: Card) -> None:
        self.cards.append(card)
