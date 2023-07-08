import pystray
from PIL import Image, ImageDraw
import time
import threading
from datetime import datetime, timedelta
import sys
import subprocess
import traceback

from times import read_csv
from options import get_options

colors = {
    'idk': 'white',
    'go': 'green',
    'iffy': 'yellow',
    'wait': 'red'
}

# Initial color of the icon
color = colors['idk']
title = "idk"


def time_until_next(times, now):
    # Convert 'now' to a time object if it's a datetime
    if isinstance(now, datetime):
        now = now.time()

    # Initialize min_diff to a large value
    min_diff = timedelta(days=1)

    for time in times:
        # Calculate the difference between the time and now
        if time > now:
            diff = datetime.combine(
                datetime.today(), time) - datetime.combine(datetime.today(), now)
            # Update min_diff if this difference is the smallest non-negative difference so far
            if diff < min_diff:
                min_diff = diff

    return min_diff.total_seconds() / 60  # Return the difference in minutes


def create_image():
    """Creates a new image with the current color"""
    # Generate an image and a draw instance
    image = Image.new('RGB', (64, 64), color)
    dc = ImageDraw.Draw(image)
    return image


def setup(icon):
    """Sets the icon to visible"""
    icon.visible = True
    update_icon(icon)


def update_icon(icon):
    """Updates the icon color based on the current time"""
    global color

    options = get_options('./options.yaml')

    while True:
        now = datetime.now()
        departures = read_csv('times.csv')
        time_left = time_until_next(departures, now)

        if time_left > options['wait'] or time_left < options['iffy']:
            color = colors['wait']
        elif time_left > options['go']:
            color = colors['go']
        elif time_left > options['iffy']:
            color = colors['iffy']
        else:
            color = colors['idk']

        icon.icon = create_image()
        icon.title = f"{options['route']}\nDeparts in {time_left:.1f} min"

        # Wait for a while before the next update
        time.sleep(15)


def donothing():
    pass


def main():
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
        except Exception as e:
            print(traceback.extract_tb(e))


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        main()
    else:
        # Use pythonw to start this script as a background process
        # Pass --background argument to indicate that the script is now running as a background process
        subprocess.Popen(['pythonw', __file__, '--background'])

        # Exit the parent process
        sys.exit(0)
