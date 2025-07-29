from dotenv import get_key

from imports.emulator import Emulator
from imports.screentail import Screentail
from pynput.keyboard import Controller, Key

import imports.utils as utils
import time


class BaseInterface:
    my_emulator = None
    my_keyboard = Controller()

    def __init__(self, emulator: Emulator):
        self.my_emulator = emulator

        self.message_area_position = (18, -80)

        self.message_area_dimensions = (
            self.my_emulator.screen_dimensions[0] - (self.message_area_position[0] * 2),
            65,
        )

        self.emulator_speed_multiplier = (
            float(get_key(".env", "EMULATOR_SPEED_MULTIPLIER")) or 1.0
        )

    def release_keys(self):
        """
        Releases any keys that might have gotten stuck during a force-quit.
        """

        keyboard = Controller()
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        keyboard.release(Key.up)
        keyboard.release(Key.down)

    def do_long_press(self, key, duration: float):
        """
        Simulates a long key press for the specified duration.

        Args:
            key (str): The key to press (e.g., 'x', 'z', Key.right, Key.left, etc).
            duration (int): The duration to hold the key down, in seconds.
        """

        keyboard = Controller()

        # Press the key down, wait, then release.
        keyboard.press(key)
        time.sleep(duration * self.emulator_speed_multiplier)
        keyboard.release(key)

    def do_sleep(self, duration: float):
        time.sleep(duration * self.emulator_speed_multiplier)

    def do_walk_right(self, num_seconds: float = 2):
        """
        Tells the character to walk to the right for 2 seconds. Used primarily
        for patrolling.
        """

        self.do_long_press(Key.right, num_seconds)

    def do_walk_left(self, num_seconds: float = 2):
        """
        Tells the character to walk to the left for 2 seconds. Used primarily
        for patrolling.
        """

        self.do_long_press(Key.left, num_seconds)

    def get_message_text(
        self,
        custom_x=None,
        custom_y=None,
        custom_width=None,
        custom_height=None,
    ):
        """
        Gets the text in the message area (e.g., "you landed a pokemon", "not
        even a nibble", etc).

        Args:
            custom_x (int or None): The custom X coordinate to use.
            custom_y (int or None): The custom Y coordinate to use.
            custom_width (int or None): The custom width to use.
            custom_height (int or None): The custom height to use.

        Returns:
            string: The text, in lower case.
        """

        # On mGBA, this value should be 18.
        x = int(custom_x) if custom_x else self.message_area_position[0]

        # On mGBA, this value should be height - 80.
        y_offset = self.my_emulator.screen_dimensions[1] + self.message_area_position[1]
        y = y_offset + int(custom_y) if custom_y else y_offset

        # On mGBA, this value should be ~450.
        width = custom_width if custom_width else self.message_area_dimensions[0]

        # On mGBA, this value should be 60.
        height = custom_height if custom_height else self.message_area_dimensions[1]

        # Take a screenshot of the message area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, x, y, width, height, "get-message-text.png"
        )

        # Extract the text.
        text = utils.get_ocr_text(screenshot)
        text = text.lower()

        return text

    def get_message_area_screenshot(self):
        # On mGBA, this value should be 18.
        x = self.message_area_position[0]

        # On mGBA, this value should be height - 80.
        y = self.my_emulator.screen_dimensions[1] + self.message_area_position[1]

        # On mGBA, this value should be ~450.
        width = self.message_area_dimensions[0]

        # On mGBA, this value should be 60.
        height = self.message_area_dimensions[1]

        # Take a screenshot of the message area.
        screenshot = Screentail.get_screenshot(
            self.my_emulator, x, y, width, height, "get-message-area.png"
        )

        return screenshot

    def check_is_battling(self, message_area_color: any):
        """
        Checks if the player is currently battling a pokémon.

        Args:
            message_area_color (any): The primary color of the message area.

        Returns:
            boolean: Whether the player is battling a pokémon.

        Example:
            >>> check_is_battling((255, 255, 255))
            true
        """

        # Take a screenshot of the message area.
        screenshot = self.get_message_area_screenshot()

        is_scanning_image = True
        is_battling = False

        num_total_pixels = 0
        num_target_pixels = 0

        # Loop through all pixels in the image.
        for x in range(screenshot.width):
            if not is_scanning_image:
                break

            for y in range(screenshot.height):
                if not is_scanning_image:
                    break

                # Get the RGB value of the pixel.
                pixel_color = screenshot.getpixel((x, y))

                if pixel_color == message_area_color:
                    num_target_pixels += 1

                num_total_pixels += 1

        # Assume we're battling if the # of target pixels is more than 10%.
        is_battling = num_target_pixels > num_total_pixels * 0.1

        return is_battling
