from pynput.keyboard import Controller, Key
import sys
import time

from imports.emulator import Emulator
from imports.interfaces.leaf_green import LeafGreenInterface
# from imports.screentail import Screentail

my_emulator = Emulator()
my_interface = LeafGreenInterface(my_emulator)
# my_pokedex = Pokedex()
# my_screentail = Screentail()

# Create the Controller object.
keyboard = Controller()

# Give the emulator some time to activate.
my_interface.do_sleep(0.2)

# ============================== #
# Commands
# ============================== #


def do_fishing(move_slot: int = 1, is_cinnibar_fishing: bool = False):
    """
    Tells the character to start fishing.
    """

    print("Fishing...")

    is_fishing = True

    while is_fishing:
        # Make sure the emulator window is active.
        my_emulator.activate_window()

        # Get the message text, if any.
        message_text = my_interface.get_message_text()

        if "hook" in message_text:
            my_interface.do_long_press("x", 0.5)
            my_interface.do_sleep(3)
            do_battle(move_slot=1)

            print("Resuming fishing...")
        elif "nibble" in message_text:
            print("Skipping...")
            my_interface.do_long_press("x", 0.5)
            my_interface.do_sleep(0.5)
        else:
            # Cast the line.
            my_interface.do_long_press(Key.backspace, 1)
            my_interface.do_sleep(0.5)


def do_battle(
    move_slot: int = 1,
    is_cinnibar_fishing: bool = False,
    is_power_leveling: bool = False,
):
    """
    Tells the character to start battling.
    """

    print("Preparing for battle...")

    is_battling = True

    while is_battling:
        my_emulator.activate_window()

        if not my_interface.check_is_battling(
            (41, 82, 107)
        ) and not my_interface.check_is_battling((255, 255, 255)):
            print("The battle appears to have ended.")
            is_battling = False
            break

        else:
            # Get the message text, if any.
            message_text = my_interface.get_message_text()

            if "appeared" in message_text:
                if is_power_leveling:
                    # Swap to and throw out our stronger pokémon.
                    print("Swapping pokémon...")
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(4)
                    my_interface.do_long_press(Key.down, 0.5)
                    my_interface.do_sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(2)
                    my_interface.do_long_press(Key.right, 0.5)
                    my_interface.do_sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(0.5)
                else:
                    # Throw out our pokémon.
                    print("Throwing pokémon...")
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(0.5)
                    my_interface.do_long_press("x", 0.5)
                    my_interface.do_sleep(0.5)

            if "what will" in message_text:
                print("Attacking pokémon...")
                my_interface.do_long_press("x", 0.5)
                my_interface.do_sleep(0.5)

                if move_slot == 2:
                    my_interface.do_long_press(Key.right, 0.5)
                    my_interface.do_sleep(0.5)

                if move_slot == 3:
                    my_interface.do_long_press(Key.down, 0.5)
                    my_interface.do_sleep(0.5)

                if move_slot == 4:
                    my_interface.do_long_press(Key.right, 0.5)
                    my_interface.do_sleep(0.5)
                    my_interface.do_long_press(Key.down, 0.5)
                    my_interface.do_sleep(0.5)

                my_interface.do_long_press("x", 0.5)
                my_interface.do_sleep(0.5)

            if (
                "fainted" in message_text
                or "gained" in message_text
                or "grew" in message_text
            ):
                print("Skipping...")
                my_interface.do_long_press("x", 0.5)
                my_interface.do_sleep(0.5)

            if "no pp left for" in message_text:
                print('Using secondary move...')
                my_interface.do_long_press("x", 0.5)
                my_interface.do_long_press(Key.right, 0.5)
                my_interface.do_long_press("x", 0.5)

            if "is disabled" in message_text:
                print('Move disabled. Running from battle...')
                my_interface.do_long_press("z", 0.5)
                my_interface.do_long_press("z", 0.5)
                my_interface.do_long_press(Key.right, 0.5)
                my_interface.do_long_press(Key.down, 0.5)
                my_interface.do_long_press("x", 0.5)
                my_interface.do_long_press("x", 0.5)


            # Wait between checking messages.
            my_interface.do_sleep(2)


def do_patrol():
    """
    Tells the character to start patrolling.
    """

    print("Starting patrol...")

    is_patrolling = True

    while is_patrolling:
        # Make sure the emulator window is active.
        my_emulator.activate_window()

        # Get the message text, if any.
        message_text = my_interface.get_message_text()

        if "appeared" in message_text:
            # Run the battle script.
            do_battle()

            print("Resuming patrol...")
        else:
            # Walk back and forth.
            my_interface.do_walk_left(1)
            my_interface.do_sleep(0.5)
            my_interface.do_walk_right(1)
            my_interface.do_sleep(0.5)


def do_test():
    my_interface.get_message_area_screenshot()


def parse_args(argv):
    """
    Parses arguments into a dictionary.
    """

    args = {}

    for arg in argv[1:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            args[key] = value

    return args


if __name__ == "__main__":
    args = parse_args(sys.argv)

    if not args:
        print("No arguments were passed.")
    else:
        action = args.get("action")
        move_slot = args.get("move-slot", 1)

        print(f"action => {action}")
        print(f"move_slot => {move_slot}")

        if action == "test":
            do_test()

        if action == "patrol":
            do_patrol()

        if action == "fish":
            do_fishing(move_slot=move_slot)

        if action == "battle":
            do_battle(move_slot=move_slot)
