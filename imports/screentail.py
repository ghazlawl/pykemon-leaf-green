from dotenv import get_key
from PIL import ImageGrab

from imports.emulator import Emulator


class Screentail:
    default_emulator_scale = 2

    @staticmethod
    def get_screenshot_bbox(
        emulator: Emulator, x: int, y: int, width: int, height: int
    ):
        """
        Converts the specified x, y, width, and height to a bounding box for use
        with the Pillow library.

        Args:
            emulator (Emulator): The emulator object.
            x (int): The X coordinate.
            y (int): The Y coordinate.
            width (int): The width of the box.
            height (int): The height of the box.

        Returns:
            tuple: The bounding box, as a tuple.

        Example:
            >>> _get_screenshot_bbox(my_emulator, 100, 100, 200, 100)
            (100, 100, 300, 200)
        """

        starting_x = emulator.emulator_position[0]
        starting_y = emulator.emulator_position[1] + emulator.emulator_menu_height

        emulator_scale = int(get_key(".env", "EMULATOR_SCALE"))

        scaled_x = round(x / Screentail.default_emulator_scale) * emulator_scale
        scaled_y = round(y / Screentail.default_emulator_scale) * emulator_scale
        scaled_width = round(width / Screentail.default_emulator_scale) * emulator_scale
        scaled_height = (
            round(height / Screentail.default_emulator_scale) * emulator_scale
        )

        x1 = starting_x + scaled_x
        y1 = starting_y + scaled_y
        x2 = x1 + scaled_width
        y2 = y1 + scaled_height

        return (x1, y1, x2, y2)

    @staticmethod
    def get_screenshot(
        emulator: Emulator,
        x: int,
        y: int,
        width: int,
        height: int,
        filename: str = None,
    ):
        """
        Gets a screenshot of the specified area.

        Args:
            emulator (Emulator): The emulator object.
            x (int): The X coordinate.
            y (int): The Y coordinate.
            width (int): The width of the area to capture.
            height (int): The height of the area to capture.
            filename (str): (Optional) The filename to save the screenshot to.

        Returns:
            Image: The screenshot.
        """

        # Get the bounding box.
        bbox = Screentail.get_screenshot_bbox(emulator, x, y, width, height)

        # Take the screenshot and convert to RGB.
        screenshot = ImageGrab.grab(all_screens=True, bbox=bbox)
        screenshot = screenshot.convert("RGB")

        # Save the screenshot.
        # if filename:
        #     screenshot.save(f"pillow/{filename}")

        return screenshot
