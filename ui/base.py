"""base.py
base Departomatic class
"""
from ui.common.times import read_csv, strip_time, time_until_next
from ui.common.options import get_options
from datetime import datetime
import threading

class Departomatic():
    """
    Base class for departomatic application
    """
    def __init__(self, options, times) -> None:
        self.options = get_options(options)
        self.departures = read_csv(times)
        self.annoy_start = None
        self.annoy_stop = None
        self.status = "idk"
        self.last_annoyed = None

        if "annoy" in options and options["annoy"]:
            self.enable_annoy = True
        else:
            self.enable_annoy = False

        if "annoy_start" in options and "annoy_stop" in options:
            self.annoy_start = strip_time(options['annoy_start'])
            self.annoy_stop = strip_time(options['annoy_stop'])

        self.timer = threading.Timer(15.0, self.time_checker)

    def time_checker(self):        
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
        pass

    def annoy(self, time_left):
        now = datetime.now()
        if self.should_annoy(now):
            if self.last_annoyed is None or (self.last_annoyed + datetime.timedelta(minutes=1)) < now:
                self.annoy_msg(f"Bus departs in {time_left:.1f} minutes!")
                self.last_annoyed = now

    def should_annoy(self, now):
        annoy = False
        if self.enable_annoy:
            if self.status == "go" or self.status == "iffy":
                if self.annoy_start is None and self.annoy_stop is None:
                    annoy = True
                elif now >= self.annoy_start and now <= self.annoy_stop:
                    annoy = True
        return annoy

    def annoy_msg(self, message):
        pass

    def run(self):
        """
        Start the application
        """
        self.time_checker()
