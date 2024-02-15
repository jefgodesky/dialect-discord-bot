from card.classes import Card


class TestCard:
    def test_creates_card(self):
        card = Card()
        assert isinstance(card, Card)

    def test_create_voice_card(self):
        card = Card("voice", 1)
        assert card.deck_type == "voice"
        assert card.index == 1

    def test_create_age1_card(self):
        card = Card("age1", 1)
        assert card.deck_type == "age1"
        assert card.index == 1

    def test_create_age2_card(self):
        card = Card("age2", 1)
        assert card.deck_type == "age2"
        assert card.index == 1

    def test_create_age3_card(self):
        card = Card("age3", 1)
        assert card.deck_type == "age3"
        assert card.index == 1

    def test_create_legacy_card(self):
        card = Card("legacy", 1)
        assert card.deck_type == "legacy"
        assert card.index == 1

    def test_filename(self):
        card = Card("legacy", 1)
        assert card.filename == "legacy01.png"
