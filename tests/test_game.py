from collections import Counter
from unittest.mock import patch, mock_open, MagicMock

from discord import Member
import pytest

from player.classes import Player
from game.classes import Game


class TestGame:
    @pytest.fixture
    def players(self):
        return [Player(MagicMock(spec=Member)) for _ in range(3)]

    @pytest.fixture
    def game(self, players):
        return Game(players)

    @pytest.fixture
    def play(self, game):
        acct = game.players[0].account
        card_expected = game.players[0].cards[0]
        card_actual = game.play(acct, card_expected.label)
        return game, card_expected, card_actual

    @pytest.fixture
    def age1(self, game):
        game.curr_phase = 1
        for player in game.players:
            player.discard()
        game.decks["age1"].deal(3, game.players)
        return game

    @pytest.fixture
    def age2(self, game):
        game.curr_phase = 2
        for player in game.players:
            player.discard()
        game.decks["age1"].deal(2, game.players)
        game.decks["age2"].deal(1, game.players)
        return game

    @pytest.fixture
    def age3(self, game):
        game.curr_phase = 3
        for player in game.players:
            player.discard()
        game.decks["age1"].deal(1, game.players)
        game.decks["age2"].deal(1, game.players)
        game.decks["age3"].deal(1, game.players)
        return game

    @pytest.fixture
    def legacy(self, game):
        game.curr_phase = 4
        for player in game.players:
            player.discard()
        game.decks["legacy"].deal(1, game.players)
        return game

    @staticmethod
    def make_play(game: Game):
        acct = game.players[0].account
        card = game.players[0].cards[0]
        game.play(acct, card.label)
        count = Counter(card.deck_type for card in game.players[0].cards)
        return count

    def test_creates_game(self):
        game = Game([])
        assert isinstance(game, Game)

    def test_adds_players_to_game(self, game):
        assert len(game.players) == 3

    def test_knows_phases(self, game):
        assert " / ".join(game.phases) == "voice / age1 / age2 / age3 / legacy"

    def test_starts_in_phase_0(self, game):
        assert game.curr_phase == 0

    def test_starts_in_voice_phase(self, game):
        assert game.phase == "voice"

    def test_creates_decks(self, game):
        assert game.decks["voice"] is not None
        assert game.decks["age1"] is not None
        assert game.decks["age2"] is not None
        assert game.decks["age3"] is not None
        assert game.decks["legacy"] is not None

    @patch("cardlist.classes.open", new_callable=mock_open, read_data="data")
    def test_uses_one_card_list(self, open_mock, players):
        Game(players)
        assert open_mock.call_count == 1

    def test_shuffles_each_deck(self, players):
        with patch("random.shuffle") as mock_shuffle:
            game = Game(players)
            for phase in game.phases:
                mock_shuffle.assert_any_call(game.decks[phase].cards)

    def test_initiates_plays_log(self, game):
        assert len(game.plays) == 0

    def test_deals_voice_cards(self, game):
        assert all(len(player.cards) == 3 for player in game.players)
        assert all(
            all(card.deck_type == "voice" for card in player.cards)
            for player in game.players
        )

    def test_next_phase(self, game):
        assert game.next_phase == ("age1", 1)
        game.curr_phase = 1
        assert game.next_phase == ("age2", 2)
        game.curr_phase = 2
        assert game.next_phase == ("age3", 3)
        game.curr_phase = 4
        assert game.next_phase == ("legacy", 4)
        game.curr_phase = 20
        assert game.next_phase == ("legacy", 4)
        game.curr_phase = -10
        assert game.next_phase == ("age1", 1)

    def test_advance_phase(self, game):
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

    def test_advance_phase_resets_plays(self, game):
        player = game.players[0]
        card = player.cards[0]
        game.plays.append((player, card))
        assert len(game.plays) == 1
        game.advance_phase()
        assert len(game.plays) == 0

    def test_get_player_index_found(self, game):
        acct = game.players[1].account
        assert game.get_player_index(acct) == 1

    def test_get_player_index_not_found(self, game):
        acct = MagicMock(spec=Member)
        assert game.get_player_index(acct) is None

    def test_players_left(self, game):
        assert len(game.players_left) == 3

    def test_play_player_not_found(self, game):
        acct = MagicMock(spec=Member)
        assert game.play(acct, "Explorer") is None

    def test_play_card_not_found(self, game):
        acct = game.players[0].account
        assert game.play(acct, "Nope") is None

    def test_play_returns_card(self, play):
        _, card_expected, card_actual = play
        assert card_expected == card_actual

    def test_play_removes_card_from_player(self, game):
        game.curr_phase = 1
        for player in game.players:
            player.discard()
        game.decks["age1"].deal(3, game.players)
        card = game.players[0].cards[0]
        game.play(game.players[0].account, card.label)
        assert all(c.label != card for c in game.players[0].cards)

    def test_play_adds_play_to_game(self, play):
        game, _, card_actual = play
        assert len(game.plays) == 1
        assert game.plays[0][0] == game.players[0]
        assert game.plays[0][1] == card_actual

    def test_play_decrements_players_left(self, play):
        game, _, _ = play
        assert len(game.players_left) == 2

    def test_play_usually_does_not_advance_phase(self, play):
        game, _, _ = play
        assert game.phase == "voice"

    def test_play_advances_phase_when_all_have_played(self, game):
        for player in game.players:
            assert game.phase == "voice"
            game.play(player.account, player.cards[0].label)
        assert game.phase == "age1"
        assert len(game.plays) == 0

    def test_play_voice_deals_age1(self, game):
        count = self.make_play(game)
        assert len(game.players[0].cards) == 3
        assert count["age1"] == 3

    def test_play_age1_deals_age2(self, age1):
        count = self.make_play(age1)
        assert len(age1.players[0].cards) == 3
        assert count["age1"] == 2
        assert count["age2"] == 1

    def test_play_age2_deals_age3(self, age2):
        count = self.make_play(age2)
        assert len(age2.players[0].cards) == 3
        assert count["age1"] in [2, 1]
        assert count["age2"] in [1, 0]
        assert count["age3"] == 1

    def test_play_age3_deals_legacy(self, age3):
        count = self.make_play(age3)
        assert len(age3.players[0].cards) == 1
        assert count["legacy"] == 1

    def test_play_legacy_does_not_draw(self, legacy):
        count = self.make_play(legacy)
        assert len(legacy.players[0].cards) == 0
        assert count["legacy"] == 0
