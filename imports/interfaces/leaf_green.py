from imports.emulator import Emulator
from imports.interfaces.base import BaseInterface
from imports.screentail import Screentail


class LeafGreenInterface(BaseInterface):
    def __init__(self, emulator: Emulator):
        super().__init__(emulator)

    def get_screenshot(self, emulator: Emulator):
        """
        This is a test function.
        """

        Screentail.get_screenshot(
            self.my_emulator,
            0,
            0,
            emulator.screen_dimensions[0],
            emulator.screen_dimensions[1],
            "screenshot.png",
        )
