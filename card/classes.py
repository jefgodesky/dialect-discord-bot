from cardlist.classes import CardList, DeckType


class Card:
    def __init__(
        self,
        deck_type: DeckType = "voice",
        index: int = 1,
        card_list: CardList = CardList(),
    ):
        self.deck_type = deck_type
        self.index = index
        self.card_list = card_list

    def __repr__(self):
        return self.label

    @property
    def filename(self):
        return self.deck_type + str(self.index).zfill(2) + ".png"

    @property
    def label(self):
        return self.card_list.get(self.deck_type, self.index)
