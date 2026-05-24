from dataclasses import dataclass

from Options import FreeText, PerGameCommonOptions, Range

class FilePath(FreeText):
    pass

# Options to over/under allocate how many cross letters are in the multiworld
class LetterAllocPercent(Range):
    default = 100
    range_start = 0
    range_end = 9999999

# What fraction of clues to start with available
class StartingPercent(Range):
    default = 10
    range_start = 0
    range_end = 9999999

# Option to overallocate how many clues are in the multiworld
# (This applies to non-starting clues)
class ClueAllocPercent(Range):
    default = 120
    range_start = 100
    range_end = 9999999


# Fraction of item rewards that should be crossword clues (vs cross letters)
class ClueItemFraction(Range):
    default = 20
    range_start = 0
    range_end = 100
    


@dataclass
class CrosswordOptions(PerGameCommonOptions):
    puz_file_path: FilePath
    puz_file_contents: FreeText
    # Can be over 100%
    cross_letter_alloc_percent: LetterAllocPercent
    # How many clues at game start
    starting_percent: StartingPercent
    clue_alloc_percent: ClueAllocPercent
    clue_item_fraction: ClueItemFraction
    


 