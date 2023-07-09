"""windows.py
Windows-only implementation of departomatic
"""
import time
import threading
from datetime import datetime

import rumps
from PIL import Image, ImageDraw

from ui.base import Departomatic
from ui.common.times import read_csv, time_until_next

import rumps
import threading
import os
from PIL import Image

icons = {
    'go': './ui/icons/macos/go.icns',
    'wait': './ui/icons/macos/wait.icns',
    'iffy': './ui/icons/macos/iffy.icns',
    'idk': './ui/icons/macos/idk.icns'
}


class MenubarApp(rumps.App):
    def __init__(self, *args, **kwargs):
        super(MenubarApp, self).__init__(*args, **kwargs)
        self.icon_paths = [icons['go'], icons['wait']]
        self.icon_index = 0
        self.timer = threading.Timer(0.15, self.change_icon)
        self.timer.start()
        # Add non-clickable text box to menu
        self.menu = [rumps.MenuItem(
            "Non-clickable text", callback=None), None]
        self.menu['Non-clickable text'].set_callback(None)

    def change_icon(self):
        self.icon = self.icon_paths[self.icon_index]
        self.icon_index = (self.icon_index + 1) % len(self.icon_paths)
        self.timer = threading.Timer(30.0, self.change_icon)
        self.timer.start()

    def quit(self, sender):
        if self.timer:
            self.timer.cancel()
        super(MenubarApp, self).quit(sender)


class App(rumps.App, Departomatic):
    """
    System try icon application showing when to leave for the bus
    """

    def __init__(self, options, times):
        Departomatic.__init__(self, options, times)
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
        if self.timer:
            self.timer.cancel()
        rumps.App.quit(self, sender)
