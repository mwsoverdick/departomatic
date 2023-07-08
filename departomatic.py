"""departomatic.py

Creates a Windows system tray icon to let you know when to leave for the bus
"""

import time
import threading
import sys
import subprocess
from datetime import datetime, timedelta

import pystray
from PIL import Image, ImageDraw

from times import read_csv
from options import get_options

colors = {
    'idk': 'white',
    'go': 'green',
    'iffy': 'yellow',
    'wait': 'red'
}

# Initial color of the icon
COLOR = colors['idk']
TITLE = "idk"


def time_until_next(departures, now):
    """Get time until next bus departure

    Args:
        departures (List[datetime.time]): List of departure times
        now (datetime): datetime.now()

    Returns:
        integer: Minutes until next departure
    """
    # Convert 'now' to a time object if it's a datetime
    if isinstance(now, datetime):
        now = now.time()

    # Initialize min_diff to a large value
    min_diff = timedelta(days=1)

    for departure in departures:
        # Calculate the difference between the time and now
        if departure > now:
            diff = datetime.combine(
                datetime.today(), departure) - datetime.combine(datetime.today(), now)
            # Update min_diff if this difference is the smallest non-negative difference so far
            if diff < min_diff:
                min_diff = diff

    return min_diff.total_seconds() / 60  # Return the difference in minutes


class Departomatic():

    def __init__(self, options, times) -> None:
        self.color = colors['idk']
        self.options = get_options(options)
        self.departures = read_csv(times)

        # Create a new system tray icon
        self.icon = pystray.Icon(
            "test_icon", self.create_image(), "Departomatic")
        # Start a new thread that updates the icon
        threading.Thread(target=self.update_icon, args=(self.icon,)).start()

        self.icon.menu = pystray.Menu(pystray.MenuItem(
            self.options['route'], lambda: donothing))

    def run(self):
        # Run the system tray icon
        self.icon.run(self.setup)

    def create_image(self):
        """Creates a new image with the current color"""
        # Generate an image and a draw instance
        image = Image.new('RGB', (64, 64), self.color)
        ImageDraw.Draw(image)
        return image

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
                self.color = colors['wait']
            elif time_left > self.options['go']:
                self.color = colors['go']
            elif time_left > self.options['iffy']:
                self.color = colors['iffy']
            else:
                self.color = colors['idk']

            icon.icon = self.create_image()
            icon.title = f"{self.options['route']}\nDeparts in {time_left:.1f} min"

            # Wait for a while before the next update
            time.sleep(15)


def donothing():
    """Does nothing
    """


def main():
    """Main program loop, runs indefinitely
    """
    departo = Departomatic('./options.yaml', './times.csv')
    departo.run()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        main()
    else:
        # Use pythonw to start this script as a background process
        # Pass --background argument to indicate that the script is
        # now running as a background process
        subprocess.Popen(['pythonw', __file__, '--background'])

        # Exit the parent process
        sys.exit(0)
