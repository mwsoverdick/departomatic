"""windows.py
Windows-only implementation of departomatic
"""
import time
import threading
from datetime import datetime

import pystray
from PIL import Image, ImageDraw

from ui.base import Departomatic
from ui.common.times import time_until_next

icons = {
    'go': './ui/icons/windows/go.png',
    'wait': './ui/icons/windows/wait.png',
    'iffy': './ui/icons/windows/iffy.png',
    'idk': './ui/icons/windows/idk.png'
}


class App(Departomatic):
    """
    System try icon application showing when to leave for the bus
    """

    def __init__(self, options, times) -> None:
        super().__init__(options, times)

        # Create a new system tray icon
        self.icon = pystray.Icon(
            "test_icon", Image.open(icons['idk']), "Departomatic")
        # Start a new thread that updates the icon
        threading.Thread(target=self.update_icon, args=(self.icon,)).start()

        self.icon.menu = pystray.Menu(pystray.MenuItem(
            self.options['route'], None))

    def run(self):
        """
        Start the system tray icon
        """
        # Run the system tray icon
        self.icon.run(self.setup)

    def setup(self, icon):
        """Sets the icon to visible"""
        icon.visible = True
        self.update_icon(icon)

    def update_icon(self, icon):
        """Updates the icon color based on the current time"""

        while True:
            now = datetime.now()
            time_left = time_until_next(self.departures, now)

            if time_left > self.options['wait'] or time_left < self.options['iffy']:
                self.color = icons['wait']
            elif time_left > self.options['go']:
                self.color = icons['go']
            elif time_left > self.options['iffy']:
                self.color = icons['iffy']
            else:
                self.color = icons['idk']

            icon.icon = Image.open(self.color)
            icon.title = f"{self.options['route']}\nDeparts in {time_left:.1f} min"

            # Wait for a while before the next update
            time.sleep(15)
