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
        self.phases: List[DeckType] = ["voice", "age1", "age2", "age3", "legacy"]
        self.curr_phase = 0

        self.decks = {}
        for deck in self.phases:
            self.decks[deck] = Deck(deck)

    @property
    def phase(self):
        return self.phases[self.curr_phase]

    def play(self, member: Member, card: Card):
        for i, (player, hand, played_card) in enumerate(self.players):
            if player == member:
                self.players[i] = (player, hand, card)
                break

        if all(player[2] is not None for player in self.players):
            self.advance_phase()

    def advance_phase(self):
        self.curr_phase = min(self.curr_phase + 1, len(self.phases) - 1)
