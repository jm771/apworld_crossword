from dataclasses import dataclass

from Options import FreeText, NumericOption, PerGameCommonOptions, Range

class FilePath(FreeText):
    pass

class LetterAllocPercent(Range):
    default = 100
    range_start = 0
    range_end = 9999999

class StartingPercent(Range):
    default = 10
    range_start = 0
    range_end = 9999999

class ClueAllocPercent(Range):
    default = 110
    range_start = 0
    range_end = 9999999


@dataclass
class CrosswordOptions(PerGameCommonOptions):
    puz_file_path: FilePath
    puz_file_contents: FreeText
    # Can be over 100%
    cross_letter_alloc_percent: LetterAllocPercent
    # How many clues at game start
    starting_percent: StartingPercent
    # Only need to collect 9/11ths of clue items to have all clues unlocked
    clue_alloc_percent: ClueAllocPercent
    


 