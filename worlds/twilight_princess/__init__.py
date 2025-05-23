from collections.abc import Mapping
from typing import Any, ClassVar

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from BaseClasses import MultiWorld, Tutorial
from Items import ITEM_TABLE, TWWItem, item_name_groups
from Locations import LOCATION_TABLE, TWWLocation
from options import tp_option_groups, TPOptions
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess

VERSION: tuple[int, int, int] = (0, 5, 1)


def run_client() -> None:
    """
    Launch the Twilight Princess client.
    """
    print("Running Twilight Princess Client")
    from .TPClient import main

    launch_subprocess(main, name="TwilightPrincessClient")


components.append(
    Component(
        "Twilight Princess Client", func=run_client, component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".aptww")
    )
)


class TPWeb(WebWorld):
    """
    This class handles the web interface for Twilight Princess.

    The web interface includes the setup guide and the options page for generating YAMLs.
    """

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the Archipelago Twilight Princess software on your computer.",
            "English",
            "setup_en.md",
            "setup/en",
            ["WritingHusky"],
        )
    ]
    theme = "grass"
    option_groups = tp_option_groups
    rich_text_options_doc = True


class TPWorld(World):
    """
    Join Link and Midna on their adventure through Hyrule in Twilight Princess.
    """

    options_dataclass = TPOptions
    options: TPOptions

    game: ClassVar[str] = "Twilight Princess"
    topology_present: bool = True

    item_name_to_id: ClassVar[dict[str, int]] = {
        name: TWWItem.get_apid(data.code) for name, data in ITEM_TABLE.items() if data.code is not None
    }
    location_name_to_id: ClassVar[dict[str, int]] = {
        name: TWWLocation.get_apid(data.code) for name, data in LOCATION_TABLE.items() if data.code is not None
    }

    item_name_groups: ClassVar[dict[str, set[str]]] = item_name_groups

    required_client_version: tuple[int, int, int] = (0, 5, 1)

    web: ClassVar[TPWeb] = TPWeb()

    origin_region_name: str = "The Great Sea"

    # create_items = generate_itempool

    # set_rules = set_rules

    def __init__(self, *args, **kwargs):
        super(TPWorld, self).__init__(*args, **kwargs)
        #
        # self.progress_locations: set[str] = set()
        # self.nonprogress_locations: set[str] = set()
        #
        # self.dungeon_local_item_names: set[str] = set()
        # self.dungeon_specific_item_names: set[str] = set()
        # self.dungeons: dict[str, Dungeon] = {}
        #
        # self.useful_pool: list[str] = []
        # self.filler_pool: list[str] = []
        #
        # self.charts = ChartRandomizer(self)
        # self.entrances = EntranceRandomizer(self)
        # self.boss_reqs = RequiredBossesRandomizer(self)

    def _determine_progress_and_nonprogress_locations(self) -> tuple[set[str], set[str]]:
        """
        Determine which locations are progress and nonprogress in the world based on the player's options.

        :return: A tuple of two sets, the first containing the names of the progress locations and the second containing
        the names of the nonprogress locations.
        """
        #
        # def add_flag(option: Toggle, flag: TWWFlag) -> TWWFlag:
        #     return flag if option else TWWFlag.ALWAYS
        #
        # options = self.options
        #
        # enabled_flags = TWWFlag.ALWAYS
        # enabled_flags |= add_flag(options.progression_dungeons, TWWFlag.DUNGEON | TWWFlag.BOSS)
        # enabled_flags |= add_flag(options.progression_tingle_chests, TWWFlag.TNGL_CT)
        # enabled_flags |= add_flag(options.progression_dungeon_secrets, TWWFlag.DG_SCRT)
        # enabled_flags |= add_flag(options.progression_puzzle_secret_caves, TWWFlag.PZL_CVE)
        # enabled_flags |= add_flag(options.progression_combat_secret_caves, TWWFlag.CBT_CVE)
        # enabled_flags |= add_flag(options.progression_savage_labyrinth, TWWFlag.SAVAGE)
        # enabled_flags |= add_flag(options.progression_great_fairies, TWWFlag.GRT_FRY)
        # enabled_flags |= add_flag(options.progression_short_sidequests, TWWFlag.SHRT_SQ)
        # enabled_flags |= add_flag(options.progression_long_sidequests, TWWFlag.LONG_SQ)
        # enabled_flags |= add_flag(options.progression_spoils_trading, TWWFlag.SPOILS)
        # enabled_flags |= add_flag(options.progression_minigames, TWWFlag.MINIGME)
        # enabled_flags |= add_flag(options.progression_battlesquid, TWWFlag.SPLOOSH)
        # enabled_flags |= add_flag(options.progression_free_gifts, TWWFlag.FREE_GF)
        # enabled_flags |= add_flag(options.progression_mail, TWWFlag.MAILBOX)
        # enabled_flags |= add_flag(options.progression_platforms_rafts, TWWFlag.PLTFRMS)
        # enabled_flags |= add_flag(options.progression_submarines, TWWFlag.SUBMRIN)
        # enabled_flags |= add_flag(options.progression_eye_reef_chests, TWWFlag.EYE_RFS)
        # enabled_flags |= add_flag(options.progression_big_octos_gunboats, TWWFlag.BG_OCTO)
        # enabled_flags |= add_flag(options.progression_expensive_purchases, TWWFlag.XPENSVE)
        # enabled_flags |= add_flag(options.progression_island_puzzles, TWWFlag.ISLND_P)
        # enabled_flags |= add_flag(options.progression_misc, TWWFlag.MISCELL)
        #
        # progress_locations: set[str] = set()
        # nonprogress_locations: set[str] = set()
        # for location, data in LOCATION_TABLE.items():
        #     if data.flags & enabled_flags == data.flags:
        #         progress_locations.add(location)
        #     else:
        #         nonprogress_locations.add(location)
        # assert progress_locations.isdisjoint(nonprogress_locations)
        #
        # return progress_locations, nonprogress_locations

    def generate_early(self) -> None:
        """
        Run before any general steps of the MultiWorld other than options.
        """
        # options = self.options
        #
        # # Determine which locations are progression and which are not from options.
        # self.progress_locations, self.nonprogress_locations = self._determine_progress_and_nonprogress_locations()
        #
        # for dungeon_item in ["randomize_smallkeys", "randomize_bigkeys", "randomize_mapcompass"]:
        #     option = getattr(options, dungeon_item)
        #     if option == "local":
        #         options.local_items.value |= self.item_name_groups[option.item_name_group]
        #     elif option.in_dungeon:
        #         self.dungeon_local_item_names |= self.item_name_groups[option.item_name_group]
        #         if option == "dungeon":
        #             self.dungeon_specific_item_names |= self.item_name_groups[option.item_name_group]
        #         else:
        #             self.options.local_items.value |= self.dungeon_local_item_names

    # create_dungeons = create_dungeons

    def setup_base_regions(self) -> None:
        """
        Create and connect all the necessary regions in the multiworld and establish the access rules for entrances.
        """
        #
        # def get_access_rule(region: str) -> str:
        #     snake_case_region = region.lower().replace("'", "").replace(" ", "_")
        #     return f"can_access_{snake_case_region}"
        #
        # multiworld = self.multiworld
        # player = self.player
        #
        # # "The Great Sea" region contains all locations that are not in a randomizable region.
        # great_sea_region = Region("The Great Sea", player, multiworld)
        # multiworld.regions.append(great_sea_region)

        # Add all randomizable regions.
        # for _entrance in ALL_ENTRANCES:
        #     multiworld.regions.append(Region(_entrance.entrance_name, player, multiworld))
        # for _exit in ALL_EXITS:
        #     multiworld.regions.append(Region(_exit.unique_name, player, multiworld))
        #
        # # Connect the dungeon, secret caves, and fairy fountain regions to the "The Great Sea" region.
        # for entrance in DUNGEON_ENTRANCES + SECRET_CAVE_ENTRANCES + FAIRY_FOUNTAIN_ENTRANCES:
        #     great_sea_region.connect(
        #         self.get_region(entrance.entrance_name),
        #         rule=lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
        #             state, player
        #         ),
        #     )

        # Connect nested regions with their parent region.
        # for entrance in MINIBOSS_ENTRANCES + BOSS_ENTRANCES + SECRET_CAVE_INNER_ENTRANCES:
        #     parent_region_name = entrance.entrance_name.split(" in ")[-1]
        #     # Consider Hyrule Castle and Forsaken Fortress as part of The Great Sea (regions are not randomizable).
        #     if parent_region_name in ["Hyrule Castle", "Forsaken Fortress"]:
        #         parent_region_name = "The Great Sea"
        #     parent_region = self.get_region(parent_region_name)
        #     parent_region.connect(
        #         self.get_region(entrance.entrance_name),
        #         rule=lambda state, entrance=entrance.entrance_name: getattr(Macros, get_access_rule(entrance))(
        #             state, player
        #         ),
        #     )

    def create_regions(self) -> None:
        """
        Create and connect regions for the Twilight Princess world.

        This method first randomizes the charts and picks the required bosses if these options are enabled.
        It then loops through all the world's progress locations and creates the locations, assigning dungeon locations
        to their respective dungeons.
        Finally, the flags for sunken treasure locations are updated as appropriate, and the entrances are randomized
        if that option is enabled.
        """
        # self.setup_base_regions()
        #
        # player = self.player
        # options = self.options
        #
        # # Set up sunken treasure locations, randomizing the charts if necessary.
        # self.charts.setup_progress_sunken_treasure_locations()
        #
        # # Select required bosses.
        # if options.required_bosses:
        #     self.boss_reqs.randomize_required_bosses()
        #     self.progress_locations -= self.boss_reqs.banned_locations
        #     self.nonprogress_locations |= self.boss_reqs.banned_locations
        #
        # # Create the dungeon classes.
        # self.create_dungeons()
        #
        # # Assign each location to their region.
        # # Progress locations are sorted for deterministic results.
        # for location_name in sorted(self.progress_locations):
        #     data = LOCATION_TABLE[location_name]
        #
        #     region = self.get_region(data.region)
        #     location = TWWLocation(player, location_name, region, data)
        #
        #     # Additionally, assign dungeon locations to the appropriate dungeon.
        #     if region.name in self.dungeons:
        #         location.dungeon = self.dungeons[region.name]
        #     elif region.name in MINIBOSS_EXIT_TO_DUNGEON and not options.randomize_miniboss_entrances:
        #         location.dungeon = self.dungeons[MINIBOSS_EXIT_TO_DUNGEON[region.name]]
        #     elif region.name in BOSS_EXIT_TO_DUNGEON and not options.randomize_boss_entrances:
        #         location.dungeon = self.dungeons[BOSS_EXIT_TO_DUNGEON[region.name]]
        #     elif location.name in [
        #         "Forsaken Fortress - Phantom Ganon",
        #         "Forsaken Fortress - Chest Outside Upper Jail Cell",
        #         "Forsaken Fortress - Chest Inside Lower Jail Cell",
        #         "Forsaken Fortress - Chest Guarded By Bokoblin",
        #         "Forsaken Fortress - Chest on Bed",
        #     ]:
        #         location.dungeon = self.dungeons["Forsaken Fortress"]
        #     region.locations.append(location)
        #
        # # Correct the flags of the sunken treasure locations if the charts are randomized.
        # self.charts.update_chart_location_flags()
        #
        # # Connect the regions in the multiworld. Randomize entrances to exits if the option is set.
        # self.entrances.randomize_entrances()

    def pre_fill(self) -> None:
        """
        Apply special fill rules before the fill stage.
        """
        # Ban the Bait Bag slot from having bait.
        # if "The Great Sea - Beedle's Shop Ship - 20 Rupee Item" in self.progress_locations:
        #     beedle_20 = self.get_location("The Great Sea - Beedle's Shop Ship - 20 Rupee Item")
        #     add_item_rule(beedle_20, lambda item: item.name not in ["All-Purpose Bait", "Hyoi Pear"])
        #
        # # Also, the same item should not appear more than once on the Rock Spire Isle shop ship.
        # locations = [f"Rock Spire Isle - Beedle's Special Shop Ship - {v} Rupee Item" for v in [500, 950, 900]]
        # if all(loc in self.progress_locations for loc in locations):
        #     rock_spire_shop_ship_locations = [self.get_location(location_name) for location_name in locations]
        #
        #     for i in range(len(rock_spire_shop_ship_locations)):
        #         curr_loc = rock_spire_shop_ship_locations[i]
        #         other_locs = rock_spire_shop_ship_locations[:i] + rock_spire_shop_ship_locations[i + 1:]
        #
        #         add_item_rule(
        #             curr_loc,
        #             lambda item, locations=other_locs: (
        #                                                        item.game == "Twilight Princess"
        #                                                        and all(
        #                                                    location.item is None or item.name != location.item.name for
        #                                                    location in locations)
        #                                                )
        #                                                or (
        #                                                        item.game != "Twilight Princess"
        #                                                        and all(
        #                                                    location.item is None or location.item.game == "Twilight Princess"
        #                                                    for location in locations
        #                                                )
        #                                                ),
        #         )

    @classmethod
    def stage_pre_fill(cls, world: MultiWorld) -> None:
        """
        Class method used to correctly place dungeon items for Twilight Princess worlds.

        :param world: The MultiWorld.
        """
        # from .randomizers.Dungeons import fill_dungeons_restrictive
        #
        # fill_dungeons_restrictive(world)

    def generate_output(self, output_directory: str) -> None:
        """
        Create the output APTWW file that is used to randomize the ISO.

        :param output_directory: The output directory for the APTWW file.
        """
        # multiworld = self.multiworld
        # player = self.player
        #
        # # Determine the current arrangement for charts.
        # # Create a list where the original island number is the index, and the value is the new island number.
        # # Without randomized charts, this array would be just an ordered list of the numbers 1 to 49.
        # # With randomized charts, the new island number is where the chart for the original island now leads.
        # chart_name_to_island_number = {
        #     chart_name: island_number for island_number, chart_name in self.charts.island_number_to_chart_name.items()
        # }
        # charts_mapping: list[int] = []
        # for i in range(1, 49 + 1):
        #     original_chart_name = ISLAND_NUMBER_TO_CHART_NAME[i]
        #     new_island_number = chart_name_to_island_number[original_chart_name]
        #     charts_mapping.append(new_island_number)
        #
        # # Output seed name and slot number to seed RNG in randomizer client.
        # output_data = {
        #     "Version": list(VERSION),
        #     "Seed": multiworld.seed_name,
        #     "Slot": player,
        #     "Name": self.player_name,
        #     "Options": {},
        #     "Required Bosses": self.boss_reqs.required_boss_item_locations,
        #     "Locations": {},
        #     "Entrances": {},
        #     "Charts": charts_mapping,
        # }
        #
        # # Output relevant options to file.
        # for field in fields(self.options):
        #     output_data["Options"][field.name] = getattr(self.options, field.name).value
        #
        # # Output which item has been placed at each location.
        # locations = multiworld.get_locations(player)
        # for location in locations:
        #     if location.name != "Defeat Ganondorf":
        #         if location.item:
        #             item_info = {
        #                 "player": location.item.player,
        #                 "name": location.item.name,
        #                 "game": location.item.game,
        #                 "classification": location.item.classification.name,
        #             }
        #         else:
        #             item_info = {"name": "Nothing", "game": "Twilight Princess", "classification": "filler"}
        #         output_data["Locations"][location.name] = item_info
        #
        # # Output the mapping of entrances to exits.
        # all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        # entrances = multiworld.get_entrances(player)
        # for entrance in entrances:
        #     assert entrance.parent_region is not None
        #     if entrance.parent_region.name in all_entrance_names:
        #         assert entrance.connected_region is not None
        #         output_data["Entrances"][entrance.parent_region.name] = entrance.connected_region.name
        #
        # # Output the plando details to file.
        # file_path = os.path.join(output_directory, f"{multiworld.get_out_file_name_base(player)}.aptww")
        # with open(file_path, "w") as f:
        #     f.write(yaml.dump(output_data, sort_keys=False))

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        """
        Fill in additional information text into locations, displayed when hinted.

        :param hint_data: A dictionary of mapping a player ID to a dictionary mapping location IDs to the extra hint
        information text. This dictionary should be modified as a side-effect of this method.
        """
        # Create a mapping of island names to numbers for sunken treasure hints.
        # island_name_to_number = {v: k for k, v in ISLAND_NUMBER_TO_NAME.items()}
        #
        # hint_data[self.player] = {}
        # for location in self.multiworld.get_locations(self.player):
        #     if location.address is not None and location.item is not None:
        #         # Regardless of ER settings, always hint at the outermost entrance for every "interior" location.
        #         zone_exit = self.entrances.get_zone_exit_for_item_location(location.name)
        #         if zone_exit is not None:
        #             outermost_entrance = self.entrances.get_outermost_entrance_for_exit(zone_exit)
        #             assert outermost_entrance is not None and outermost_entrance.island_name is not None
        #             hint_data[self.player][location.address] = outermost_entrance.island_name
        #
        #         # Hint at which chart leads to the sunken treasure for these locations.
        #         if location.name.endswith(" - Sunken Treasure"):
        #             island_name = location.name.removesuffix(" - Sunken Treasure")
        #             island_number = island_name_to_number[island_name]
        #             chart_name = self.charts.island_number_to_chart_name[island_number]
        #             hint_data[self.player][location.address] = chart_name

    def determine_item_classification(self, name: str) -> IC | None:
        """
        Determine the adjusted classification of an item. The classification of an item may be affected by which options
        are enabled or disabled.

        :param name: The name of the item.
        :return: The adjusted classification of the item. If there is no adjustment from the default, returns `None`.
        """
        # TODO: Calculate nonprogress items dynamically
        # adjusted_classification = None
        # if not self.options.progression_big_octos_gunboats and name == "Progressive Quiver":
        #     adjusted_classification = IC.useful
        # if self.options.sword_mode == "swords_optional" and name == "Progressive Sword":
        #     adjusted_classification = IC.useful
        # if not self.options.enable_tuner_logic and name == "Tingle Tuner":
        #     adjusted_classification = IC.useful
        #
        # if not self.options.progression_dungeons and name.endswith(" Key"):
        #     adjusted_classification = IC.filler
        # if not self.options.progression_dungeons and name in ("Command Melody", "Earth God's Lyric", "Wind God's Aria"):
        #     adjusted_classification = IC.filler
        # if not self.options.progression_short_sidequests and name in ("Maggie's Letter", "Moblin's Letter"):
        #     adjusted_classification = IC.filler
        # if (
        #         not self.options.progression_short_sidequests
        #         and self.options.progression_long_sidequests
        #         and name == "Progressive Picto Box"
        # ):
        #     adjusted_classification = IC.filler
        # if not self.options.progression_spoils_trading and name == "Spoils Bag":
        #     adjusted_classification = IC.filler
        # if not self.options.progression_triforce_charts and name.startswith("Triforce Chart"):
        #     adjusted_classification = IC.filler
        # if not self.options.progression_treasure_charts and name.startswith("Treasure Chart"):
        #     adjusted_classification = IC.filler
        # if not self.options.progression_misc and name.endswith("Tingle Statue"):
        #     adjusted_classification = IC.filler
        #
        # return adjusted_classification

    def create_item(self, name: str) -> TWWItem:
        """
        Create an item for this world type and player.

        :param name: The name of the item to create.
        :raises KeyError: If an invalid item name is provided.
        """
        # if name in ITEM_TABLE:
        #     return TWWItem(name, self.player, ITEM_TABLE[name], self.determine_item_classification(name))
        # raise KeyError(f"Invalid item name: {name}")

    def get_filler_item_name(self) -> str:
        """
        This method is called when the item pool needs to be filled with additional items to match the location count.

        :return: The name of a filler item from this world.
        """
        # # If there are still useful items to place, place those first.
        # if len(self.useful_pool) > 0:
        #     return self.useful_pool.pop()
        #
        # # If there are still vanilla filler items to place, place those first.
        # if len(self.filler_pool) > 0:
        #     return self.filler_pool.pop()
        #
        # # Use the same weights for filler items used in the base randomizer.
        # filler_consumables = ["Yellow Rupee", "Red Rupee", "Purple Rupee", "Orange Rupee", "Joy Pendant"]
        # filler_weights = [3, 7, 10, 15, 3]
        # return self.multiworld.random.choices(filler_consumables, weights=filler_weights, k=1)[0]

    def get_pre_fill_items(self) -> list[Item]:
        """
        Return items that need to be collected when creating a fresh `all_state` but don't exist in the multiworld's
        item pool.

        :return: A list of pre-fill items.
        """
        # res = []
        # if self.dungeon_local_item_names:
        #     for dungeon in self.dungeons.values():
        #         for item in dungeon.all_items:
        #             if item.name in self.dungeon_local_item_names:
        #                 res.append(item)
        # return res

    def fill_slot_data(self) -> Mapping[str, Any]:
        """
        Return the `slot_data` field that will be in the `Connected` network package.

        This is a way the generator can give custom data to the client.
        The client will receive this as JSON in the `Connected` response.

        :return: A dictionary to be sent to the client when it connects to the server.
        """
        # slot_data = {
        #     "progression_dungeons": self.options.progression_dungeons.value,
        #     "progression_tingle_chests": self.options.progression_tingle_chests.value,
        #     "progression_dungeon_secrets": self.options.progression_dungeon_secrets.value,
        #     "progression_puzzle_secret_caves": self.options.progression_puzzle_secret_caves.value,
        #     "progression_combat_secret_caves": self.options.progression_combat_secret_caves.value,
        #     "progression_savage_labyrinth": self.options.progression_savage_labyrinth.value,
        #     "progression_great_fairies": self.options.progression_great_fairies.value,
        #     "progression_short_sidequests": self.options.progression_short_sidequests.value,
        #     "progression_long_sidequests": self.options.progression_long_sidequests.value,
        #     "progression_spoils_trading": self.options.progression_spoils_trading.value,
        #     "progression_minigames": self.options.progression_minigames.value,
        #     "progression_battlesquid": self.options.progression_battlesquid.value,
        #     "progression_free_gifts": self.options.progression_free_gifts.value,
        #     "progression_mail": self.options.progression_mail.value,
        #     "progression_platforms_rafts": self.options.progression_platforms_rafts.value,
        #     "progression_submarines": self.options.progression_submarines.value,
        #     "progression_eye_reef_chests": self.options.progression_eye_reef_chests.value,
        #     "progression_big_octos_gunboats": self.options.progression_big_octos_gunboats.value,
        #     "progression_triforce_charts": self.options.progression_triforce_charts.value,
        #     "progression_treasure_charts": self.options.progression_treasure_charts.value,
        #     "progression_expensive_purchases": self.options.progression_expensive_purchases.value,
        #     "progression_island_puzzles": self.options.progression_island_puzzles.value,
        #     "progression_misc": self.options.progression_misc.value,
        #     "randomize_mapcompass": self.options.randomize_mapcompass.value,
        #     "randomize_smallkeys": self.options.randomize_smallkeys.value,
        #     "randomize_bigkeys": self.options.randomize_bigkeys.value,
        #     "sword_mode": self.options.sword_mode.value,
        #     "required_bosses": self.options.required_bosses.value,
        #     "num_required_bosses": self.options.num_required_bosses.value,
        #     "chest_type_matches_contents": self.options.chest_type_matches_contents.value,
        #     "included_dungeons": self.options.included_dungeons.value,
        #     "excluded_dungeons": self.options.excluded_dungeons.value,
        #     # "trap_chests": self.options.trap_chests.value,
        #     "hero_mode": self.options.hero_mode.value,
        #     "logic_obscurity": self.options.logic_obscurity.value,
        #     "logic_precision": self.options.logic_precision.value,
        #     "enable_tuner_logic": self.options.enable_tuner_logic.value,
        #     "randomize_dungeon_entrances": self.options.randomize_dungeon_entrances.value,
        #     "randomize_secret_cave_entrances": self.options.randomize_secret_cave_entrances.value,
        #     "randomize_miniboss_entrances": self.options.randomize_miniboss_entrances.value,
        #     "randomize_boss_entrances": self.options.randomize_boss_entrances.value,
        #     "randomize_secret_cave_inner_entrances": self.options.randomize_secret_cave_inner_entrances.value,
        #     "randomize_fairy_fountain_entrances": self.options.randomize_fairy_fountain_entrances.value,
        #     "mix_entrances": self.options.mix_entrances.value,
        #     "randomize_enemies": self.options.randomize_enemies.value,
        #     # "randomize_music": self.options.randomize_music.value,
        #     "randomize_starting_island": self.options.randomize_starting_island.value,
        #     "randomize_charts": self.options.randomize_charts.value,
        #     # "hoho_hints": self.options.hoho_hints.value,
        #     # "fishmen_hints": self.options.fishmen_hints.value,
        #     # "korl_hints": self.options.korl_hints.value,
        #     # "num_item_hints": self.options.num_item_hints.value,
        #     # "num_location_hints": self.options.num_location_hints.value,
        #     # "num_barren_hints": self.options.num_barren_hints.value,
        #     # "num_path_hints": self.options.num_path_hints.value,
        #     # "prioritize_remote_hints": self.options.prioritize_remote_hints.value,
        #     "swift_sail": self.options.swift_sail.value,
        #     "instant_text_boxes": self.options.instant_text_boxes.value,
        #     "reveal_full_sea_chart": self.options.reveal_full_sea_chart.value,
        #     "add_shortcut_warps_between_dungeons": self.options.add_shortcut_warps_between_dungeons.value,
        #     "skip_rematch_bosses": self.options.skip_rematch_bosses.value,
        #     "remove_music": self.options.remove_music.value,
        #     "death_link": self.options.death_link.value,
        # }
        #
        # # Add entrances to `slot_data`. This is the same data that is written to the .aptww file.
        # all_entrance_names = [en.entrance_name for en in ALL_ENTRANCES]
        # entrances = {
        #     entrance.parent_region.name: entrance.connected_region.name
        #     for entrance in self.multiworld.get_entrances(self.player)
        #     if entrance.parent_region is not None
        #        and entrance.connected_region is not None
        #        and entrance.parent_region.name in all_entrance_names
        # }
        # slot_data["entrances"] = entrances
        #
        # return slot_data
