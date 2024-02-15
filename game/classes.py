from typing import List, Optional
from discord import Member

from card.classes import Card
from cardlist.classes import CardList, DeckType
from deck.classes import Deck
from hand.classes import Hand


class Game:
    def __init__(self, players: List[Member]):
        self.card_list = CardList()
        hands = [Hand(card_list=self.card_list) for _ in players]
        played: List[Optional[Card]] = [None for _ in players]
        self.players = list(zip(players, hands, played))
        self.phase = "voice"

        decks: List[DeckType] = ["voice", "age1", "age2", "age3", "legacy"]
        self.decks = {}
        for deck in decks:
            self.decks[deck] = Deck(deck)
