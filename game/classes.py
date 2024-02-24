from typing import List, Optional, Tuple

from discord import Member
from conlang_tools.language.classes import Language

from card.classes import Card
from cardlist.classes import CardList, DeckType
from deck.classes import Deck
from player.classes import Player


class Game:
    def __init__(self, players: List[Player], base_language: Optional[str] = None):
        self.card_list = CardList()
        self.players = players
        self.phases: List[DeckType] = ["voice", "age1", "age2", "age3", "legacy"]
        self.curr_phase = 0
        self.plays: List[Tuple[Player, Card]] = []
        self.decks = {phase: Deck(phase, self.card_list) for phase in self.phases}
        for phase in self.phases:
            self.decks[phase].shuffle()
        self.decks["voice"].deal(3, self.players)

        if base_language:
            try:
                self.base_language = Language.load(base_language)
            except FileNotFoundError:
                print(f"Could not find languages/{base_language}.yaml")
                self.base_language = None

    @property
    def phase(self):
        return self.phases[self.curr_phase]

    @property
    def next_phase(self) -> Tuple[DeckType, int]:
        curr_phase = max(min(self.curr_phase, len(self.phases) - 1), 0)
        index = min(curr_phase + 1, len(self.phases) - 1)
        return self.phases[index], index

    @property
    def players_left(self) -> List[Player]:
        played = [player for player, card in self.plays]
        return list(filter(lambda player: player not in played, self.players))

    def join(self, new_player: Player) -> bool:
        if self.phase != "voice":
            return False

        self.players.append(new_player)
        self.decks["voice"].deal(3, [new_player])
        return True

    def advance_phase(self) -> None:
        _, next_phase = self.next_phase
        self.curr_phase = next_phase
        self.plays = []

    def get_player_index(self, account: Member) -> Optional[int]:
        for index, player in enumerate(self.players):
            if player.account == account:
                return index
        return None

    def play(self, account: Member, label: str) -> Optional[Card]:
        player_index = self.get_player_index(account)
        if player_index is None:
            return

        card_index = self.players[player_index].get_card_index(label)
        if card_index is None:
            return

        player = self.players[player_index]
        card = player.cards[card_index]
        player.cards.remove(card)
        self.plays.append((player, card))

        draw = ["voice", "age1", "age2", "age3"]
        if self.phase in draw:
            redeal = {"age1": 3, "legacy": 1}
            if self.next_phase[0] in list(redeal.keys()):
                player.discard()
                num = redeal[self.next_phase[0]]
                self.decks[self.next_phase[0]].deal(num, [player])
            else:
                player.deal([self.decks[self.next_phase[0]].draw()])

        if len(self.players_left) == 0:
            self.advance_phase()

        return card
