from unittest.mock import MagicMock

from deck.classes import Deck
from hand.classes import Hand
from game.classes import Game


class TestGame:
    def test_creates_game(self):
        game = Game([])
        assert isinstance(game, Game)

    def test_create_game_with_players(self):
        players = [MagicMock() for _ in range(3)]
        game = Game(players)
        assert len(game.players) == 3
        assert all(isinstance(player[0], MagicMock) for player in game.players)
        assert all(isinstance(player[1], Hand) for player in game.players)
        assert all(player[2] is None for player in game.players)

    def test_has_phases(self):
        game = Game([])
        assert " / ".join(game.phases) == "voice / age1 / age2 / age3 / legacy"

    def test_starts_with_voices(self):
        game = Game([])
        assert game.phase == "voice"

    def test_creates_a_voices_deck(self):
        game = Game([])
        assert isinstance(game.decks["voice"], Deck)
        assert game.decks["voice"].deck_type == "voice"

    def test_creates_age1_deck(self):
        game = Game([])
        assert isinstance(game.decks["age1"], Deck)
        assert game.decks["age1"].deck_type == "age1"

    def test_creates_age2_deck(self):
        game = Game([])
        assert isinstance(game.decks["age2"], Deck)
        assert game.decks["age2"].deck_type == "age2"

    def test_creates_age3_deck(self):
        game = Game([])
        assert isinstance(game.decks["age3"], Deck)
        assert game.decks["age3"].deck_type == "age3"

    def test_creates_legacy_deck(self):
        game = Game([])
        assert isinstance(game.decks["legacy"], Deck)
        assert game.decks["legacy"].deck_type == "legacy"

    def test_advance_phase(self):
        game = Game([])
        assert game.phase == "voice"
        game.advance_phase()
        assert game.phase == "age1"
        game.advance_phase()
        assert game.phase == "age2"
        game.advance_phase()
        assert game.phase == "age3"
        game.advance_phase()
        assert game.phase == "legacy"
        game.advance_phase()
        assert game.phase == "legacy"
