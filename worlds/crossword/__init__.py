import dataclasses
import math
import random
from typing import Optional

from BaseClasses import Item, ItemClassification, Region, Tutorial

from worlds.AutoWorld import WebWorld, World
from worlds.crossword.Types import Clue, CrossLetter, ParsedPuz, SlotData

from .Items import CrosswordItem, item_table
from .Locations import CrosswordLocation, location_table

from .Options import CrosswordOptions
from .puz_parser import parse_puz

class CrosswordWeb(WebWorld):
    tutorials = [
        # Tutorial(
        #     "Multiworld Setup Guide",
        #     "A guide to setting up Crossword. This guide covers single-player, multiworld, and website.",
        #     "English",
        #     "setup_en.md",
        #     "setup/en",
        #     ["jm771"],
        # )
    ]

def get_vibes(hope, madness):
    sub_vibes = [6, 12, 3, 81, 23]
    product = 1
    for vibe in sub_vibes:
        product *= vibe
    return int(f"{math.pow(product, 1/len(sub_vibes)):.0f}") * (-1) ** madness

def parse_puz_for_rando(data: bytes) -> ParsedPuz:
    clue_map, letter_list = parse_puz(data)
    cross_letters = [CrossLetter(clueid, index, letter) for letter, locs in letter_list for clueid, index in locs]
    clues = [Clue(clueid.direction, clueid.number, clueinfo.clue, clueinfo.answer) for clueid, clueinfo in clue_map.items()]
    return ParsedPuz(clues, cross_letters)

def get_perc(a, b):
    return (a * b + 99) / 100

class CrosswordWorld(World):
    """
    Solve a Crossword puzzle!
    """

    game: str = "Crossword"
    options_dataclass = CrosswordOptions

    web = CrosswordWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = location_table

    ap_world_version = "0.0.0"

    parsed_crossword: Optional[ParsedPuz]

    def generate_early(self):
        options: CrosswordOptions = self.options
        if options.puz_file_contents.value:
            raise Exception("Haven't yet supported puz files contents field")
        if not options.puz_file_path.value:
            raise Exception("must provide puz file path")
        with open(options.puz_file_path.value, "rb") as f:
            data = f.read()


        self.parsed_crossword = parse_puz_for_rando(data)
        self.random.shuffle(self.parsed_crossword.clues)
        self.random.shuffle(self.parsed_crossword.cross_letters)

    def create_regions(self):        
        menu = Region("Menu", self.player, self.multiworld)
    
        menu.locations = [CrosswordLocation(self.player, key, value, menu) for key, value in location_table.items()]
        n_starting = self.get_n_starting()

        n_clues = len(self.parsed_crossword.clues)
        n_clue_unlocks = get_perc(n_clues, self.options.clue_alloc_percent.value)

        for i, loc in enumerate(menu.locations):
            n_items_required = math.ceil((i - n_starting + 1) * n_clue_unlocks / (n_clues - n_starting))
            loc.access_rule = lambda state, nitems=n_items_required: state.has("Clue Unlock", self.player, nitems) if n_items_required > 0 else lambda state: True
        
        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"Solved a clue {n_clues-1}"
        self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        self.multiworld.regions += [menu]

    def create_items(self):
        hope = 1
        vibes = get_vibes(hope, 7)
        options: CrosswordOptions = self.options
        n_clue_unlocks = get_perc(len(self.parsed_crossword.clues), options.clue_alloc_percent.value)
        n_cross_letter_unlocks = get_perc(len(self.parsed_crossword.cross_letters), options.cross_letter_alloc_percent.value)
        self.multiworld.itempool += [self.create_item("Clue Unlock") for i in range (0 + vibes, n_clue_unlocks + vibes)]
        self.multiworld.itempool += [self.create_item("Cross Letter") for i in range (0, n_cross_letter_unlocks)]



    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = CrosswordItem(name, item_data.classification, item_data.code, self.player)
        return item


    def fill_slot_data(self): 
        slot_dataclass = SlotData(self.get_n_starting(), self.parsed_crossword.clues, self.parsed_crossword.cross_letters)
        return dataclasses.to_dict(slot_dataclass)
    
    def get_n_starting(self):
        return get_perc(self.options.starting_percent.value, len(self.parsed_crossword.clues))
    # def open_page(url):
    #     import webbrowser
    #     import re
    #     # Extract slot, pass, host, and port from the URL
    #     # URL format: archipelago://slot:pass@host:port
    #     match = re.match(r"archipelago://([^:]+):([^@]+)@([^:]+):(\d+)", url)
    #     if not match:
    #         raise ValueError("Invalid URL format")
        
    #     slot, password, host, port = match.groups()
    #     if password == "None":
    #         webbrowser.open(f"http://Crossword-ap.netlify.app/?hostport={host}:{port}&name={slot}")
    #     else:
    #         webbrowser.open(f"http://Crossword-ap.netlify.app/?hostport={host}:{port}&name={slot}&password={password}")

    # components.append(
    #     Component(
    #         "Crossword AutoLaunch",
    #         func=open_page,
    #         component_type=component_type.HIDDEN,
    #         supports_uri=True,
    #         game_name="Crossword"
    #     )
    # )