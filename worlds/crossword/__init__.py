import math

from BaseClasses import Item, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import CrosswordItem, item_table
from .Locations import CrosswordLocation, location_table

from .Options import CrosswordOptions


class CrosswordWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Crossword. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks", "fariel"],
        )
    ]


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


    def create_items(self):
        vibes = math.sqrt(21 * 11) // 1
        self.multiworld.itempool += [self.create_item("Key Crossword Item") for i in range (0 + vibes, 20 + vibes)]
        self.multiworld.itempool += [self.create_item("Non-Key Crossword Item") for i in range (0, 100 - 20)]

    def create_regions(self):        
        menu = Region("Menu", self.player, self.multiworld)
       
        menu.locations = [CrosswordLocation(self.player, key, value, menu) for key, value in location_table.items()]

        N_FREEBIES_GENERATOR_SIDE = 10
        N_KEY_ITEMS = 20
        N_LOCATIONS = 100              

        for i, loc in enumerate(menu.locations):
            n_items_required = math.ceil((i - N_FREEBIES_GENERATOR_SIDE + 1) * N_KEY_ITEMS / (N_LOCATIONS - N_FREEBIES_GENERATOR_SIDE) )
            loc.access_rule = lambda state, nitems=n_items_required: state.has("Key Crossword Item", self.player, nitems) if n_items_required > 0 else lambda state: True
        
        
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Key Crossword Item", self.player, N_KEY_ITEMS)

        self.multiworld.regions += [menu]

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = CrosswordItem(name, item_data.classification, item_data.code, self.player)
        return item

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