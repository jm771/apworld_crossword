from dataclasses import dataclass

from Options import PerGameCommonOptions


@dataclass
class CrosswordOptions(PerGameCommonOptions):
    puz_file_path: str
    puz_file_contents: str
    # Can be over 100%
    cross_letter_alloc_percent: float = 100
    # How many clues at game start
    starting_percent: float = 10
    # Only need to collect 9/11ths of clue items to have all clues unlocked
    clue_alloc_percent: float = 110
    


 