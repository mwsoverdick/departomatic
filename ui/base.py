"""base.py
base Departomatic class
"""
from ui.common.times import read_csv
from ui.common.options import get_options


class Departomatic():
    def __init__(self, options, times) -> None:
        self.options = get_options(options)
        self.departures = read_csv(times)

    def run(self):
        """
        Start the application
        """
