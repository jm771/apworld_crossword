from dataclasses import dataclass

from Options import PerGameCommonOptions


@dataclass
class CrosswordOptions(PerGameCommonOptions):
    puz_file_path: str
    puz_file_contents: str

 