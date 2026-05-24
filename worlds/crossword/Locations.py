import typing

from BaseClasses import Location

class CrosswordLocation(Location):
    game: str = "Crossword"

    def __init__(self, player: int, name: str, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)

MAX_N_CLUES = 1000

def make_location_name(i):
    return f"Solved a clue {i}"

location_table = {make_location_name(i): i for i in range(0, MAX_N_CLUES)}