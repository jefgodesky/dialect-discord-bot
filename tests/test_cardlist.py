from cardlist.classes import CardList


class TestCardList:
    def test_creates_card_list(self):
        list = CardList()
        assert isinstance(list, CardList)

    def test_loads_labels(self):
        labels = CardList()
        assert labels.get("voice", 1) == "Explorer"
