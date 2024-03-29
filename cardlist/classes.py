from typing import Literal
import yaml

DeckType = Literal["voice", "age1", "age2", "age3", "legacy"]


class CardList:
    def __init__(self):
        with open("cardlist.yaml") as file:
            try:
                self.data = yaml.safe_load(file)
            except yaml.YAMLError as err:
                print(err)

    def get(self, deck_type: DeckType, index: int) -> str:
        return self.data[deck_type][index - 1]
