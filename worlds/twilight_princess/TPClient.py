import asyncio
import time
import traceback

import Utils
import dolphin_memory_engine
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from typing import TYPE_CHECKING, Any, Optional

from NetUtils import NetworkItem

if TYPE_CHECKING:
    import kvui

CONNECTION_REFUSED_GAME_STATUS = (
    "Dolphin failed to connect. Please load a randomized ROM for Twilight Princess. Trying again in 5 seconds..."
)
CONNECTION_REFUSED_SAVE_STATUS = (
    "Dolphin failed to connect. Please load into the save file. Trying again in 5 seconds..."
)
CONNECTION_LOST_STATUS = (
    "Dolphin connection was lost. Please restart your emulator and make sure Twilight Princess is running."
)
CONNECTION_CONNECTED_STATUS = "Dolphin connected successfully."
CONNECTION_INITIAL_STATUS = "Dolphin connection has not been initiated."

CURR_HEALTH_ADDR = 0x804061C2
CURR_NODE_ADDR = 0X80406B38
SLOT_NAME_ADDR = 0x80406374


class TPCommandProcessor(ClientCommandProcessor):
    """
    Command processor for the Twilight Princess client.

    This class handles all commands that are specific to the Twilight Princess client.
    """

    def __init__(self, ctx: CommonContext):
        """
        Initialize the command processor with the provided context.

        :param ctx: Context for the client.
        """
        super().__init__(ctx)

    def _cmd_dolphin(self) -> None:
        """
        Display the current Dolphin emulator connection status.
        """
        if isinstance(self.ctx, TPContext):
            logger.info(f"Dolphin Status: {self.ctx.dolphin_status}")


class TPContext(CommonContext):
    """
    The context for Twilight Princess client.

    This class manages all interactions with the Dolphin emulator and the Archipelago server for Twilight Princess.
    """
    command_processor = TPCommandProcessor
    game: str = "Twilight Princess"
    items_handling: int = 0b111

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        """
        Initialize the context with the provided server address and password.

        :param server_address: The address of the Archipelago server.
        :param password: The password for the server.
        """
        super().__init__(server_address, password)
        self.items_received_2: list[tuple[NetworkItem, int]] = []
        self.dolphin_sync_task: Optional[asyncio.Task[None]] = None
        self.dolphin_status: str = CONNECTION_INITIAL_STATUS
        self.awaiting_rom: bool = False
        self.last_received_index: int = -1
        self.has_send_death: bool = False

    async def disconnect(self, allow_autoreconnect: bool = False) -> None:
        """
        Disconnect from the server and stop the Dolphin synchronization task.

        :param allow_autoreconnect: Whether to allow the client to automatically reconnect to the server.
        """
        self.auth = None
        await super().disconnect(allow_autoreconnect)

    async def server_auth(self, password_requested: bool = False) -> None:
        """
        Authenticate with the Archipelago server.

        :param password_requested: Whether the server requires a password. Defaults to `False`.
        """
        if password_requested and not self.password:
            await super(TPContext, self).server_auth(password_requested)
        if not self.auth:
            if self.awaiting_rom:
                return
            self.awaiting_rom = True
            logger.info("Awaiting connection to Dolphin to get player information.")
            return
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        """
        Handle incoming packages from the server.

        :param cmd: The command received from the server.
        :param args: The command arguments.
        """
        if cmd == "Connected":
            self.items_received_2 = []
            self.last_received_index = -1
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
            # Request the connected slot's dictionary (used as a set) of visited stages.
        elif cmd == "ReceivedItems":
            if args["index"] >= self.last_received_index:
                self.last_received_index = args["index"]
                for item in args["items"]:
                    self.items_received_2.append((item, self.last_received_index))
                    self.last_received_index += 1
            self.items_received_2.sort(key=lambda v: v[1])
        elif cmd == "Retrieved":
            requested_keys_dict = args["keys"]
            # Read the connected slot's dictionary (used as a set) of visited stages.
            if self.slot is not None:
                self.slot.visited_stages = requested_keys_dict

    def on_deathlink(self, data: dict[str, Any]) -> None:
        """
        Handle a DeathLink event.

        :param data: The data associated with the DeathLink event.
        """
        super().on_deathlink(data)
        _give_death(self)

    def make_gui(self) -> type["kvui.GameManager"]:
        """
        Initialize the GUI for Twilight Princess client.

        :return: The client's GUI.
        """
        ui = super().make_gui()
        ui.base_title = "Archipelago Twilight Princess Client"
        return ui




def read_byte(console_address: int) -> int:
    """
    Read a byte from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return dolphin_memory_engine.read_byte(console_address)

def read_short(console_address: int) -> int:
    """
    Read a short from Dolphin memory.

    :param console_address: Address to read from.
    :return: The value read from memory.
    """
    return int.from_bytes(dolphin_memory_engine.read_bytes(console_address, 2), byteorder="big")

def read_string(console_address: int, strlen: int) -> str:
    """
    Read a string from Dolphin memory.

    :param console_address: Address to read from.
    :param strlen: Length of the string to read.
    :return: The string read from memory.
    """
    return dolphin_memory_engine.read_bytes(console_address, strlen).split(b"\0", 1)[0].decode()


def write_byte(console_address: int, value: int) -> None:
    """
    Write a byte to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dolphin_memory_engine.write_bytes(console_address, value)

def write_short(console_address: int, value: int) -> None:
    """
    Write a short to Dolphin memory.

    :param console_address: Address to write to.
    :param value: Value to write.
    """
    dolphin_memory_engine.write_bytes(console_address, value.to_bytes(2, byteorder="big"))


def _give_death(ctx: TPContext) -> None:
    """
    Trigger the player's death in-game by setting their current health to zero.

    :param ctx: Twilight Princess client context.
    """
    if (
            ctx.slot is not None
            and dolphin_memory_engine.is_hooked()
            and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS
            and check_ingame()
    ):
        ctx.has_send_death = True
        write_short(CURR_HEALTH_ADDR, 0)


def _give_item(ctx: TPContext, item_name: str) -> None:
    """
    Give an item to the player in-game.

    :param ctx: Twilight Princess client context.
    :param item_name: Name of the item to give.
    :return: Whether the item was successfully given.
    """
    raise NotImplementedError("This function is not yet implemented.")



async def give_items(ctx: TPContext) -> None:
    """
    Give the player all outstanding items they have yet to receive.

    :param ctx: Twilight Princess client context.
    """
    raise NotImplementedError("This function is not yet implemented.")


def check_active_node_location(location_name: str, data: TPLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that require special logic.

    :param location_name: The name of the location.
    :param data: The data associated with the location.
    :raises NotImplementedError: If an unknown location name is provided.
    """
    raise NotImplementedError("This function is not yet implemented.")


def check_regular_location(ctx: TPContext, curr_stage_id: int, data: TPLocationData) -> bool:
    """
    Check that the player has checked a given location.
    This function handles locations that only require checking that a particular bit is set.

    The check looks at the saved data for the stage at which the location is located and the data for the current stage.
    In the latter case, this data includes data that has not yet been written to the saved data.

    :param ctx: Twilight Princess client context.
    :param curr_stage_id: The current stage at which the player is.
    :param data: The data associated with the location.
    :raises NotImplementedError: If a location with an unknown type is provided.
    """
    raise NotImplementedError("This function is not yet implemented.")


async def check_locations(ctx: TPContext) -> None:
    """
    Iterate through all locations and check whether the player has checked each location.

    Update the server with all newly checked locations since the last update. If the player has completed the goal,
    notify the server.

    :param ctx: Twilight Princess client context.
    """
    raise NotImplementedError("This function is not yet implemented.")

async def check_alive() -> bool:
    """
    Check if the player is currently alive in-game.

    :return: `True` if the player is alive, otherwise `False`.
    """
    cur_health = read_short(CURR_HEALTH_ADDR)
    return cur_health > 0


async def check_death(ctx: TPContext) -> None:
    """
    Check if the player is currently dead in-game.
    If DeathLink is on, notify the server of the player's death.

    :return: `True` if the player is dead, otherwise `False`.
    """
    if ctx.slot is not None and check_ingame():
        cur_health = read_short(CURR_HEALTH_ADDR)
        if cur_health <= 0:
            if not ctx.has_send_death and time.time() >= ctx.last_death_link + 3:
                ctx.has_send_death = True
                await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of hearts.")
        else:
            ctx.has_send_death = False


def check_ingame() -> bool:
    """
    Check if the player is currently in-game.

    :return: `True` if the player is in-game, otherwise `False`.
    """
    return read_byte(CURR_NODE_ADDR) != 0xFF


async def dolphin_sync_task(ctx: TPContext) -> None:
    """
    The task loop for managing the connection to Dolphin.

    While connected, read the emulator's memory to look for any relevant changes made by the player in the game.

    :param ctx: Twilight Princess client context.
    """
    logger.info("Starting Dolphin connector. Use /dolphin for status information.")
    while not ctx.exit_event.is_set():
        try:
            if dolphin_memory_engine.is_hooked() and ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                if not check_ingame():
                    await asyncio.sleep(0.1)
                    continue
                if ctx.slot is not None:
                    if "DeathLink" in ctx.tags:
                        await check_death(ctx)
                    await give_items(ctx)
                    await check_locations(ctx)
                else:
                    if not ctx.auth:
                        ctx.auth = read_string(SLOT_NAME_ADDR, 0x40)
                    if ctx.awaiting_rom:
                        await ctx.server_auth()
                await asyncio.sleep(0.1)
            else:
                if ctx.dolphin_status == CONNECTION_CONNECTED_STATUS:
                    logger.info("Connection to Dolphin lost, reconnecting...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                logger.info("Attempting to connect to Dolphin...")
                dolphin_memory_engine.hook()
                if dolphin_memory_engine.is_hooked():
                    if dolphin_memory_engine.read_bytes(0x80000000, 6) != b"GZ2E01":
                        logger.info(CONNECTION_REFUSED_GAME_STATUS)
                        ctx.dolphin_status = CONNECTION_REFUSED_GAME_STATUS
                        dolphin_memory_engine.un_hook()
                        await asyncio.sleep(5)
                    else:
                        logger.info(CONNECTION_CONNECTED_STATUS)
                        ctx.dolphin_status = CONNECTION_CONNECTED_STATUS
                        ctx.locations_checked = set()
                else:
                    logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
                    ctx.dolphin_status = CONNECTION_LOST_STATUS
                    await ctx.disconnect()
                    await asyncio.sleep(5)
                    continue
        except Exception:
            dolphin_memory_engine.un_hook()
            logger.info("Connection to Dolphin failed, attempting again in 5 seconds...")
            logger.error(traceback.format_exc())
            ctx.dolphin_status = CONNECTION_LOST_STATUS
            await ctx.disconnect()
            await asyncio.sleep(5)
            continue


def main(connect: Optional[str] = None, password: Optional[str] = None) -> None:
    """
    Run the main async loop for the Twilight Princess client.

    :param connect: Address of the Archipelago server.
    :param password: Password for server authentication.
    """
    Utils.init_logging("Twilight Princess Client")

    async def _main(connect: Optional[str], password: Optional[str]) -> None:
        ctx = TPContext(connect, password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await asyncio.sleep(1)

        ctx.dolphin_sync_task = asyncio.create_task(dolphin_sync_task(ctx), name="DolphinSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.dolphin_sync_task:
            await asyncio.sleep(3)
            await ctx.dolphin_sync_task

    import colorama

    colorama.init()
    asyncio.run(_main(connect, password))
    colorama.deinit()


if __name__ == "__main__":
    parser = get_base_parser()
    args = parser.parse_args()
    main(args.connect, args.password)