"""windows.py
Windows-only implementation of departomatic
"""
import rumps

from pync import Notifier
from ui.base import Departomatic


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

        # Add non-clickable text box to menu for route info
        self.menu = [rumps.MenuItem(
            self.options['route'], callback=None), None]
        self.menu[self.options['route']].set_callback(None)

        self.route_info = self.menu[self.options['route']]

    def run(self, **options):
        """Start departomatic
        """
        Departomatic.run(self)
        rumps.App.run(self, **options)

    def annoy_msg(self, title, message):
        # com.mwsoverdick.departomatic used as placeholder for possible
        # app bundling later. For now, will be TERMINAL-NOTIFIER
        Notifier.notify(message,
                        title=title,
                        sound='default',
                        group="Departomatic",
                        sender='com.mwsoverdick.departomatic',
                        )

    def update_icon(self, time_left):
        """
        Changes icon when called to appropriate state for next bus departure
        """

        self.icon = icons[self.status]

        if time_left is None:
            self.route_info.title = f"{self.options['route']}\nDeparts in ??? min"
        else:
            self.route_info.title = f"{self.options['route']}\nDeparts in {time_left:.1f} min"

    def quit(self):
        """
        Rumps quit callback for quitting the application

        Args:
            sender: Sender from Rumps
        """
        Departomatic._stop(self)
