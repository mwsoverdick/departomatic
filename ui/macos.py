"""windows.py
Windows-only implementation of departomatic
"""
import threading
from datetime import datetime
import rumps

from ui.base import Departomatic
from ui.common.times import time_until_next


icons = {
    'go': './ui/icons/macos/go.icns',
    'wait': './ui/icons/macos/wait.icns',
    'iffy': './ui/icons/macos/iffy.icns',
    'idk': './ui/icons/macos/idk.icns'
}


class App(rumps.App, Departomatic):
    """
    System try icon application showing when to leave for the bus
    """

    def __init__(self, options, times):
        Departomatic.__init__(self, options, times)
        self.icon = None # Gets reinitialized in rumps init below
        rumps.App.__init__(self,
                           "Departomatic", icon=icons['idk'])
        self.timer = threading.Timer(0.15, self.change_icon)
        self.timer.start()

        # Add non-clickable text box to menu for route info
        self.menu = [rumps.MenuItem(
            self.options['route'], callback=None), None]
        self.menu[self.options['route']].set_callback(None)

        self.route_info = self.menu[self.options['route']]

    def change_icon(self):
        """
        Changes icon when called to appropriate state for next bus departure
        """
        now = datetime.now()
        time_left = time_until_next(self.departures, now)

        if time_left > self.options['wait'] or time_left < self.options['iffy']:
            self.icon = icons['wait']
        elif time_left > self.options['go']:
            self.icon = icons['go']
        elif time_left > self.options['iffy']:
            self.icon = icons['iffy']
        else:
            self.icon = icons['idk']

        self.route_info.title = f"{self.options['route']} departs in {time_left:.1f} min"

        self.timer = threading.Timer(30.0, self.change_icon)
        self.timer.start()

    def quit(self, sender):
        """
        Rumps quit callback for quitting the application

        Args:
            sender: Sender from Rumps
        """
        if self.timer:
            self.timer.cancel()
        rumps.App.quit(self, sender)
