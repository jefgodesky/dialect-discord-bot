from typing import Optional
from discord import Member
from game.classes import Game
from player.classes import Player


class GameManager:
    def __init__(self):
        self.directory = {}

    def create(self, server: int, channel: int, initiator: Member) -> bool:
        key = (server, channel)
        if key in self.directory:
            return False

        self.directory[key] = Game([Player(initiator)])
        return True

    def get(self, server: int, channel: int) -> Optional[Game]:
        key = (server, channel)
        if key in self.directory:
            return self.directory[key]
        return None

    def end(self, server: int, channel: int) -> bool:
        key = (server, channel)
        if key in self.directory:
            del self.directory[key]
            return True
        return False
