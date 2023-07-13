"""windows.py
Windows-only implementation of departomatic
"""
import time
import threading
from datetime import datetime, timedelta
from win10toast import ToastNotifier

import pystray
from PIL import Image

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
            "Starting...", Image.open(icons['idk']), "Departomatic", None)
        # Start a new thread that updates the icon
        # threading.Thread(target=self.update_icon, args=(self.icon,)).start()

    def run(self):
        """
        Start the system tray icon
        """
        # Run the system tray icon
        self.icon.run_detached()

        super().run()

    def annoy_msg(self, message):
        title = "You should probably go."
        toaster = ToastNotifier()
        toaster.show_toast(title, message, duration=2, threaded=True)

    def update_icon(self, time_left):
        """Updates the icon color based on the current time"""
        self.icon.visible = True
        self.icon.icon = Image.open(icons[self.status])
        if time_left is None:
            self.icon.title = f"{self.options['route']}\nDeparts in ??? min"
        else:
            self.icon.title = f"{self.options['route']}\nDeparts in {time_left:.1f} min"
