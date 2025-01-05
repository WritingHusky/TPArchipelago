from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple, Optional, Union

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World


def item_factory(items: Union[str, Iterable[str]], world: World) -> Union[Item, list[Item]]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    ret: list[Item] = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in ITEM_TABLE:
            ret.append(world.create_item(item))
        else:
            raise KeyError(f"Unknown item {item}")

    return ret[0] if singleton else ret


class TPItemData(NamedTuple):
    """
    This class represents the data for an item in Twilight Princess

    :param type: The type of the item (e.g., "Item", "Poe").
    :param classification: The item's classification (progression, useful, filler).
    :param code: The unique code identifier for the item.
    :param quantity: The number of this item available.
    :param item_id: The ID used to represent the item in-game.
    """

    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    item_id: Optional[int]


class TPItem(Item):
    """
    This class represents an item in Twilight Princess

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = "Twilight Princess"
    type: Optional[str]

    def __init__(self, name: str, player: int, data: TPItemData, classification: Optional[IC] = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else TPItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 2322432
        return base_id + code


ITEM_TABLE: dict[str, TPItemData] = {
    # Name:                         (Type,                  Classification,     Code,   Quantity,   Item ID)
    "Green Rupee":                  TPItemData("Rupee",      IC.filler,          0,      1,          0x01),
    "Blue Rupee":                   TPItemData("Rupee",      IC.filler,          1,      1,          0x02),
    "Yellow Rupee":                 TPItemData("Rupee",      IC.filler,          2,      1,          0x03),
    "Red Rupee":                    TPItemData("Rupee",      IC.filler,          3,      1,          0x04),
    "Purple Rupee":                 TPItemData("Rupee",      IC.filler,          4,      1,          0x05),
    "Orange Rupee":                 TPItemData("Rupee",      IC.filler,          5,      1,          0x06),
    "Silver Rupee":                 TPItemData("Rupee",      IC.filler,          6,      1,          0x07),
    "Bombs (5)":                    TPItemData("Item",       IC.filler,          7,      5,          0x0A),
    "Bombs (10)":                   TPItemData("Item",       IC.filler,          8,      1,          0x0B),
    "Bombs (20)":                   TPItemData("Item",       IC.filler,          9,      1,          0x0C),
    "Bombs (30)":                   TPItemData("Item",       IC.filler,          10,     1,          0x0D),
    "Arrows (10)":                  TPItemData("Item",       IC.filler,          11,     1,          0x0E),
    "Arrows (20)":                  TPItemData("Item",       IC.filler,          12,     1,          0x0F),
    "Arrows (30)":                  TPItemData("Item",       IC.filler,          13,     1,          0x10),
    "Seeds (50)":                   TPItemData("Item",       IC.filler,          14,     1,          0x12),
    "Water Bombs (3)":              TPItemData("Item",       IC.filler,          15,     1,          0x19),
    "Water Bombs (5)":              TPItemData("Item",       IC.filler,          16,     1,          0x16),
    "Water Bombs (10)":             TPItemData("Item",       IC.filler,          17,     1,          0x17),
    "Water Bombs (15)":             TPItemData("Item",       IC.filler,          18,     1,          0x18),
    "Bomblings (3)":                TPItemData("Item",       IC.filler,          19,     1,          0x1C),
    "Bomblings (5)":                TPItemData("Item",       IC.filler,          20,     1,          0x1A),
    "Bomblings (10)":               TPItemData("Item",       IC.filler,          21,     1,          0x1B),
    "Piece of Heart":               TPItemData("Item",       IC.filler,          22,     1,          0x21),
    "Heart Container":              TPItemData("Item",       IC.filler,          23,     1,          0x22),
    "Progressive Master Sword":     TPItemData("Item",       IC.progression,     24,     1,          0x29),
    "Ordon Shield":                 TPItemData("Item",       IC.progression,     25,     1,          0x2A),
    "Hylian Shield":                TPItemData("Item",       IC.progression,     26,     1,          0x2C),
    "Magic Armor":                  TPItemData("Item",       IC.progression,     27,     1,          0x30),
    "Zora Armor":                   TPItemData("Item",       IC.progression,     28,     1,          0x31),
    "Shadow Crystal":               TPItemData("Item",       IC.progression,     29,     1,          0x32),
    "Progressive Wallet":           TPItemData("Item",       IC.progression,     30,     1,          0x36),
    "Hawkeye":                      TPItemData("Item",       IC.progression,     31,     1,          0x3E),
    "Gale Boomerang":               TPItemData("Item",       IC.progression,     32,     1,          0x40),
    "Spinner":                      TPItemData("Item",       IC.progression,     33,     1,          0x41),
    "Ball and Chain":               TPItemData("Item",       IC.progression,     34,     1,          0x42),
    "Progressive Hero's Bow":       TPItemData("Item",       IC.progression,     35,     1,          0x43),
    "Progressive Clawshot":         TPItemData("Item",       IC.progression,     36,     1,          0x44),
    "Iron Boots":                   TPItemData("Item",       IC.progression,     37,     1,          0x45),
    "Progressive Dominion Rod":     TPItemData("Item",       IC.progression,     38,     1,          0x46),
    "Lantern":                      TPItemData("Item",       IC.progression,     39,     1,          0x48),
    "Progressive Fishing Rod":      TPItemData("Item",       IC.progression,     40,     1,          0x4A),
    "Slingshot":                    TPItemData("Item",       IC.progression,     41,     1,          0x4B),
    "Giant Bomb Bag":               TPItemData("Item",       IC.progression,     42,     1,          0x4C),

    "Victory": TPItemData("Event", IC.progression, None, 1, None),
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    TPItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {
    "Bottles": {
        "Empty Bottle (Fishing Hole Bottle)",
        "Milk (half) (Sera Bottle)",
        "Lantern Oil (Coro Bottle)",
        "Great Fairy Tears (Jovani Bottle)",
    },
    "Quest Items": {
        "Renado's Letter",
        "Invoice",
        "Wooden Statue",
        "Ilia's Charm",
    },
    "Rupees": {
        "Green Rupee",
        "Blue Rupee",
        "Yellow Rupee",
        "Red Rupee",
        "Purple Rupee",
        "Orange Rupee",
        "Silver Rupee",
    },
    "Bombs": {
        "Bombs (5)",
        "Bombs (10)",
        "Bombs (20)",
        "Bombs (30)",
        "Water Bombs (3)",
        "Water Bombs (5)",
        "Water Bombs (10)",
        "Water Bombs (15)",
        "Bomblings (3)",
        "Bomblings (5)",
        "Bomblings (10)",
    },
    "Arrows": {
        "Arrows (10)",
        "Arrows (20)",
        "Arrows (30)",
    },
    "Shields": {
        "Ordon Shield",
        "Hylian Shield",
    },
    "Tunics": {
        "Zora Armor",
        "Magic Armor",
    },
    "Bomb Bags": {
        "Empty Bomb Bag",
        "Goron Bomb Bag",
        "Giant Bomb Bag",
    },
    "Small Keys": {
        "Forest Temple Small Key",
        "Goron Mines Small Key",
        "Lakebed Temple Small Key",
        "Arbiter's Grounds Small Key",
        "Snowpeak Ruins Small Key",
        "Temple of Time Small Key",
        "City in the Sky Small Key",
        "Palace of Twilight Small Key",
        "Hyrule Castle Small Key",
        "Bublin Camp Key",
    },
    "Big Keys": {
        "Forest Temple Big Key",
        "Progressive Key Shard",
        "Lakebed Temple Big Key",
        "Arbiter's Grounds Big Key",
        "Bedroom Key",
        "Temple of Time Big Key",
        "City in the Sky Big Key",
        "Palace of Twilight Big Key",
        "Hyrule Castle Big Key",
    },
    "Maps": {
        "Forest Temple Map",
        "Goron Mines Map",
        "Lakebed Temple Map",
        "Arbiter's Grounds Map",
        "Snowpeak Ruins Map",
        "Temple of Time Map",
        "City in the Sky Map",
        "Palace of Twilight Map",
        "Hyrule Castle Map",
    },
    "Compasses": {
        "Forest Temple Compass",
        "Goron Mines Compass",
        "Lakebed Temple Compass",
        "Arbiter's Grounds Compass",
        "Snowpeak Ruins Compass",
        "Temple of Time Compass",
        "City in the Sky Compass",
        "Palace of Twilight Compass",
        "Hyrule Castle Compass",
    },
    "Bugs": {
        "Male Beetle",
        "Female Beetle",
        "Male Butterfly",
        "Female Butterfly",
        "Male Stag Beetle",
        "Female Stag Beetle",
        "Male Grasshopper",
        "Female Grasshopper",
        "Male Phasmid",
        "Female Phasmid",
        "Male Pill Bug",
        "Female Pill Bug",
        "Male Mantis",
        "Female Mantis",
        "Male Ladybug",
        "Female Ladybug",
        "Male Snail",
        "Female Snail",
        "Male Dragonfly",
        "Female Dragonfly",
        "Male Ant",
        "Female Ant",
        "Male Dayfly",
        "Female Dayfly",
    }
}
# generic groups, (Name, substring)
_simple_groups = {
    ("Poe Souls", "Poe Soul"),
    ("Heart Pieces", "Heart Piece"),
    ("Heart Containers", "Heart Container"),
    ("Small Keys", "Small Key"),
    ("Seeds", "Seeds (50)"),
    ("Swords", "Progressive Sword"),
    ("Shadow Crystal", "Shadow Crystal"),
    ("Wallets", "Progressive Wallet"),
    ("Slingshot", "Slingshot"),
    ("Bows", "Progressive Bow"),
    ("Quivers", "Progressive Quiver"),
    ("Hawkeye", "Hawkeye"),
    ("Gale Boomerang", "Gale Boomerang"),
    ("Spinner", "Spinner"),
    ("Ball and Chain", "Ball and Chain"),
    ("Dominion Rod", "Progressive Dominion Rod"),
    ("Clawshots", "Progressive Clawshot"),
    ("Iron Boots", "Iron Boots"),
    ("Horse Call", "Horse Call"),
    ("Lantern", "Lantern"),
    ("Fishing Rods", "Progressive Fishing Rod"),
    ("Aurus's Memo", "Aurus's Memo"),
    ("Ashei's Sketch", "Ashei's Sketch"),
    ("Mirrors", "Progressive Mirror Shard"),
    ("Fused Shadows", "Progressive Fused Shadow"),
    ("Hidden Skills", "Progressive Hidden Skill"),
    ("Ancient Sky Book", "Progressive Ancient Sky Book"),
    ("Links Purple Rupee", "Links Purple Rupee"),


}
for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)

del _simple_groups
