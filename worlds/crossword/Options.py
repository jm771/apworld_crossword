from dataclasses import dataclass

from Options import FreeText, NumericOption, PerGameCommonOptions

class FilePath(FreeText):
    pass

class LetterAllocPercent(NumericOption):
    default = 100

class StartingPercent(NumericOption):
    default = 10

class ClueAllocPercent(NumericOption):
    default = 110


@dataclass
class CrosswordOptions(PerGameCommonOptions):
    puz_file_path: FilePath
    puz_file_contents: str
    # Can be over 100%
    cross_letter_alloc_percent: LetterAllocPercent
    # How many clues at game start
    starting_percent: StartingPercent
    # Only need to collect 9/11ths of clue items to have all clues unlocked
    clue_alloc_percent: ClueAllocPercent
    


 