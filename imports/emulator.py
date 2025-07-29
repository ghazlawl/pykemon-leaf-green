from dotenv import get_key
import pygetwindow as gw


class Emulator:
    # emulator_menu_height = 80
    # emulator_window = None
    # emulator_dimensions = (0, 0)
    # emulator_position = (0, 0)

    # screen_dimensions = (0, 0)

    def __init__(self, window_title: str = "mGBA"):
        self.window_title = window_title
        self.emulator_window = self.get_window()

        if window_title == "mGBA":
            self.emulator_menu_height = 53
        elif window_title == "DeSmuME":
            self.emulator_menu_height = 80

        if self.emulator_window:
            self.activate_window()
            self.update_vars()

    def get_window(self):
        """
        Gets the emulator window, if any.
        """

        # Get all emulator windows, if present.
        emulator_windows = gw.getWindowsWithTitle(self.window_title)

        if len(emulator_windows) > 0:
            # Get the first emulator window.
            emulator_window = emulator_windows[0]

        # Quit the application if the emulator window doesn't exist.
        if not emulator_window:
            print("Emulator not running.")
            quit()

        # Let the user know that we found the emulator window.
        print(f"Emulator window found: {emulator_window.title}")

        return emulator_window

    def activate_window(self):
        """
        Activates (focuses) the emulator window.
        """

        self.emulator_window.activate()
        self.update_vars()

    def update_vars(self):
        """
        Updates the emulator position, screen position, and screen
        dimension local variables.
        """

        emulator_menu_height_override = get_key(".env", "EMULATOR_MENU_HEIGHT")

        if emulator_menu_height_override:
            self.emulator_menu_height = int(emulator_menu_height_override)

        self.emulator_position = (
            self.emulator_window.left + 6,
            self.emulator_window.top,
        )

        # print(f"update_vars() => emulator_position => {self.emulator_position}")

        self.emulator_dimensions = (
            self.emulator_window.width - 12,
            self.emulator_window.height - 8,
        )

        # print(f"update_vars() => emulator_dimensions => {self.emulator_dimensions}")

        self.screen_dimensions = (
            self.emulator_dimensions[0],
            int(self.emulator_dimensions[1] - self.emulator_menu_height),
        )

        # print(f"update_vars() => screen_dimensions => {self.screen_dimensions}")
