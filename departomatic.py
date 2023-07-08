"""departomatic.py

Creates a Windows system tray icon to let you know when to leave for the bus
"""

import time
import threading
import sys
import subprocess
import traceback
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


def create_image():
    """Creates a new image with the current color"""
    # Generate an image and a draw instance
    image = Image.new('RGB', (64, 64), COLOR)
    ImageDraw.Draw(image)
    return image


def setup(icon):
    """Sets the icon to visible"""
    icon.visible = True
    update_icon(icon)


def update_icon(icon):
    """Updates the icon color based on the current time"""
    global COLOR

    options = get_options('./options.yaml')

    while True:
        now = datetime.now()
        departures = read_csv('times.csv')
        time_left = time_until_next(departures, now)

        if time_left > options['wait'] or time_left < options['iffy']:
            COLOR = colors['wait']
        elif time_left > options['go']:
            COLOR = colors['go']
        elif time_left > options['iffy']:
            COLOR = colors['iffy']
        else:
            COLOR = colors['idk']

        icon.icon = create_image()
        icon.title = f"{options['route']}\nDeparts in {time_left:.1f} min"

        # Wait for a while before the next update
        time.sleep(15)


def donothing():
    """Does nothing
    """


def main():
    """Main program loop, runs indefinitely
    """
    while True:
        try:
            # Create a new system tray icon
            icon = pystray.Icon(
                "test_icon", create_image(), "Departomatic")
            # Start a new thread that updates the icon
            threading.Thread(target=update_icon, args=(icon,)).start()

            options = get_options('./options.yaml')
            icon.menu = pystray.Menu(pystray.MenuItem(
                options['route'], lambda: donothing))

            # Run the system tray icon
            icon.run(setup)
        except Exception as ex:
            print(traceback.extract_tb(ex))


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
