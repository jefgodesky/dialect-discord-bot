from typing import List
import random

from card.classes import Card, DeckType
from cardlist.classes import CardList
from hand.classes import Hand


class Deck:
    def __init__(self, deck_type: DeckType = "voice", card_list: CardList = CardList()):
        sizes = {"voice": 15, "age1": 22, "age2": 25, "age3": 14, "legacy": 6}
        self.deck_type = deck_type
        self.cards = [Card(deck_type, x + 1) for x in range(sizes[deck_type])]
        self.card_list = card_list

    def get_label(self, index: int):
        return self.card_list.get(self.deck_type, index)

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def draw(self) -> Card:
        return self.cards.pop()

    def deal(self, num: int, players: List[Hand]) -> None:
        for x in range(num):
            for player in players:
                player.draw(self.draw())
