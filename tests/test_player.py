from unittest.mock import MagicMock

import pytest
from discord import Member

from card.classes import Card
from player.classes import Player


class TestPlayer:
    @pytest.fixture
    def player(self):
        member = MagicMock(spec=Member)
        return Player(member)

    @pytest.fixture
    def player_with_voice_cards(self, player):
        cards = [Card("voice", i + 1) for i in range(3)]
        player.deal(cards)
        return player

    def test_creates_player_with_account(self, player):
        assert isinstance(player, Player)
        assert player.account is not None

    def test_creates_player_with_no_cards(self, player):
        assert len(player.cards) == 0

    def test_deal_adds_cards(self, player_with_voice_cards):
        player = player_with_voice_cards
        assert len(player.cards) == 3
        assert player.cards[0].label == "Explorer"
        assert player.cards[1].label == "Ruler"
        assert player.cards[2].label == "Jester"

    def test_discard(self, player_with_voice_cards):
        player = player_with_voice_cards
        player.discard()
        assert len(player.cards) == 0

    def test_get_card_index_found(self, player_with_voice_cards):
        player = player_with_voice_cards
        assert player.get_card_index("Ruler") == 1

    def test_get_card_index_not_found(self, player_with_voice_cards):
        player = player_with_voice_cards
        assert player.get_card_index("Celebrity") is None

    def test_play(self, player_with_voice_cards):
        player = player_with_voice_cards
        card = player.play("Ruler")
        assert isinstance(card, Card)
        assert card.label == "Ruler"
        assert len(player.cards) == 2
        assert player.cards[0].label == "Explorer"
        assert player.cards[1].label == "Jester"

    def test_play_not_found(self, player_with_voice_cards):
        player = player_with_voice_cards
        card = player.play("Celebrity")
        assert card is None
        assert len(player.cards) == 3
