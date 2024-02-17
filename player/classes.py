from typing import List, Optional

from discord import Member

from card.classes import Card


class Player:
    def __init__(self, account: Member):
        self.account = account
        self.cards = []

    def deal(self, cards: List[Card]) -> None:
        self.cards = self.cards + cards

    def discard(self) -> None:
        self.cards = []

    def play(self, label: str) -> Optional[Card]:
        index = self.get_card_index(label)
        if index is None:
            return None

        card = self.cards[index]
        self.cards.remove(card)
        return card

    def get_card_index(self, label: str) -> Optional[int]:
        for index, card in enumerate(self.cards):
            if self.cards[index].label == label:
                return index
        return None
