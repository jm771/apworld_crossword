import typing


from BaseClasses import Item, ItemClassification
from typing import Optional

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification

class CrosswordItem(Item):
    game: str = "Crossword"
    
    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int):
        self.name = name
        self.classification = classification
        self.player = player
        self.code = code
        self.location = None


item_table = {
    "Key Crossword Item": ItemData(1, ItemClassification.progression),
    "Non-Key Crossword Item": ItemData(2, ItemClassification.useful)
}
