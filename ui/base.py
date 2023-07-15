"""base.py
base Departomatic class
"""
from ui.common.times import read_csv, strip_time, time_until_next
from ui.common.options import get_options
from datetime import datetime, timedelta
import threading


class Departomatic():
    """
    Base class for departomatic application
    """
    def __init__(self, options, times) -> None:
        """
        Initialize Departomatic App

        Args:
            options: path to options.yaml
            times: path to times.csv
        """

        self.options = get_options(options)
        self.departures = read_csv(times)
        self.status = "idk"
        self.last_annoyed = None

        # Start time checking timer thread to run every 15s
        self.timer = threading.Timer(15.0, self.time_checker)

    def time_checker(self): 
        """
        Time checker thread.

        Uses departures from csv passed in constructor to see how long until
        the next bus departs. Sets internal data structures accordingly.
        """
        now = datetime.now()
        time_left = time_until_next(self.departures, now)

        if time_left > self.options['wait'] or time_left < self.options['iffy']:
            self.status = "wait"
        elif time_left > self.options['go']:
            self.status = "go"
        elif time_left > self.options['iffy']:
            self.status = "iffy"
        else:
            self.status = "idk"

        self.annoy(time_left)

        self.update_icon(time_left)

        self.timer = threading.Timer(15.0, self.time_checker)
        self.timer.start()

    def update_icon(self, time_left):
        """
        Child class specific icon updating procedure.

        Must be implemented by child class

        Args:
            time_left: minutes until next departure will be passed in

        Raises:
            NotImplementedError: This is not implemented in the base class
        """
        raise NotImplementedError("update_icon not implemented!")

    def annoy(self, time_left):
        """
        Given configuration of options.yaml, this will annoy the user to leave.

        Currently only annoys if feature is enable and status is 'go' or 'iffy'

        Args:
            time_left: minutes until next departure
        """
        title = "You should probably go."
        now = datetime.now()
        if self.should_annoy(now):
            if self.last_annoyed is None or (self.last_annoyed + timedelta(minutes=1)) < now:
                self.annoy_msg(title, f"Bus departs in {time_left:.1f} minutes!")
                self.last_annoyed = now

    def should_annoy(self, now):
        """
        Annoy logic.

        Args:
            now: the time now

        Returns:
            True/False: Do annoy/Don't annoy
        """
        annoy = False
        now = now.time()
        if self.options["annoy"]["enable"]:
            if self.status == "go" or self.status == "iffy":
                if self.options["annoy"]["start"] is None and self.options["annoy"]["stop"] is None:
                    annoy = True
                elif now >= self.options["annoy"]["start"] and now <= self.options["annoy"]["stop"]:
                    annoy = True
        return annoy

    def annoy_msg(self, title, message):
        """
        Child class specific annoy procedure.

        Called when a user should be annoyed.

        Args:
            title: Title of annoying message
            message: Annoying message

        Raises:
            NotImplementedError: This is not implemented in the base class
        """
        raise NotImplementedError("annoy_msg not implemented")

    def _stop(self):
        """
        Stops the recursive timers
        """
        if self.timer:
            self.timer.cancel()

    def run(self):
        """
        Start the application
        """
        self.time_checker()
