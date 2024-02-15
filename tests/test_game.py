from collections import Counter
from unittest.mock import MagicMock

import pytest

from card.classes import Card
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

    def test_deals_voices(self):
        players = [MagicMock() for _ in range(3)]
        game = Game(players)
        for player in game.players:
            assert len(player[1].cards) == 3
            assert all(card.deck_type == "voice" for card in player[1].cards)

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

    def test_next_phase(self):
        game = Game([])
        assert game.next_phase() == 1

    def test_next_phase_max(self):
        game = Game([])
        game.curr_phase = 20
        assert game.next_phase() == len(game.phases) - 1

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

    @pytest.fixture
    def play_game(self):
        players = [MagicMock() for _ in range(3)]
        game = Game(players)
        assert game.players[0][2] is None
        assert game.players[1][2] is None
        return game

    def test_play(self, play_game):
        card = play_game.players[0][1].cards[0]
        play_game.play(play_game.players[0][0], card)
        assert play_game.players[0][2] == card
        assert play_game.players[1][2] is None

    def test_play_advances_phase(self, play_game):
        for player in play_game.players:
            assert play_game.phase == "voice"
            play_game.play(player[0], Card())
        assert play_game.phase == "age1"

    def test_advancing_to_age1_deals_cards(self, play_game):
        play_game.advance_phase()
        for player in play_game.players:
            assert len(player[1].cards) == 3
            assert all(card.deck_type == "age1" for card in player[1].cards)

    def test_get_player_index(self, play_game):
        assert play_game.get_player_index(play_game.players[0][0]) == 0

    def test_get_player(self, play_game):
        assert play_game.get_player(play_game.players[0][0]) == play_game.players[0]

    def test_deal(self, play_game):
        play_game.deal("age1")
        for player in play_game.players:
            assert len(player[1].cards) == 3
            assert all(card.deck_type == "age1" for card in player[1].cards)

    @staticmethod
    def draw(phase: int, game: Game):
        game.curr_phase = phase
        game.draw(game.players[0][0])
        hand = game.players[0][1]
        count = Counter(card.deck_type for card in hand.cards)
        return hand, count

    def test_draw_voice(self, play_game):
        hand, count = self.draw(0, play_game)
        assert len(hand.cards) == 3
        assert count["voice"] == 3

    def test_draw_age1(self, play_game):
        hand, count = self.draw(1, play_game)
        assert len(hand.cards) == 4
        assert count["voice"] == 3
        assert count["age2"] == 1

    def test_draw_age2(self, play_game):
        hand, count = self.draw(2, play_game)
        assert len(hand.cards) == 4
        assert count["voice"] == 3
        assert count["age3"] == 1

    def test_draw_age3(self, play_game):
        hand, count = self.draw(3, play_game)
        assert len(hand.cards) == 4
        assert count["voice"] == 3
        assert count["legacy"] == 1

    def test_draw_legacy(self, play_game):
        hand, count = self.draw(4, play_game)
        assert len(hand.cards) == 3
        assert count["voice"] == 3

    def test_draw_too_late(self, play_game):
        hand, count = self.draw(25, play_game)
        assert len(hand.cards) == 3
        assert count["voice"] == 3
