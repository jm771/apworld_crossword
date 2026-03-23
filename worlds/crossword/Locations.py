import typing

from BaseClasses import Location

class CrosswordLocation(Location):
    game: str = "Crossword"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)

location_table = {f"Solved some clues {i}": i for i in range(1, 101)}