from unittest.mock import MagicMock
from discord import Member
from game.classes import Game
from gamemanager.classes import GameManager


class TestGameManager:
    def test_creates_gamemanager(self):
        manager = GameManager()
        assert isinstance(manager, GameManager)

    def test_creates_directory(self):
        manager = GameManager()
        assert isinstance(manager.directory, dict)

    def test_create_game(self):
        manager = GameManager()
        requester = MagicMock(spec=Member)
        result = manager.create(123456789, 987654321, requester)
        game = manager.directory[(123456789, 987654321)]
        assert result is True
        assert isinstance(game, Game)
        assert len(game.players) == 1
        assert game.players[0].account == requester

    def test_create_game_already_in_progress(self):
        manager = GameManager()
        requester = MagicMock(spec=Member)
        manager.create(123456789, 987654321, requester)
        assert manager.create(123456789, 987654321, requester) is False

    def test_get_game_found(self):
        manager = GameManager()
        requester = MagicMock(spec=Member)
        manager.create(123456789, 987654321, requester)
        assert isinstance(manager.get(123456789, 987654321), Game)

    def test_get_game_not_found(self):
        manager = GameManager()
        assert manager.get(123456789, 987654321) is None

    def test_end_game(self):
        manager = GameManager()
        requester = MagicMock(spec=Member)
        manager.create(123456789, 987654321, requester)
        assert manager.end(123456789, 987654321) is True
        assert manager.get(123456789, 987654321) is None

    def test_end_game_not_found(self):
        manager = GameManager()
        assert manager.end(123456789, 987654321) is False
        assert manager.get(123456789, 987654321) is None
