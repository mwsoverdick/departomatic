"""times.py
bus stop schedule interface.
"""

import csv
from datetime import datetime


def read_csv(filename):
    """Reads a CSV of bus stop times and returns them as datetime objects 

    Args:
        filename (str): Patht to csv file

    Returns:
        List[datetime.time()]: list of bus stop times
    """
    with open(filename, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header
        stoptimes = [datetime.strptime(row[0].strip().replace('a.m.', 'AM').replace(
            'p.m.', 'PM'), '%I:%M %p').time() for row in reader]
    return stoptimes


if __name__ == '__main__':
    # usage
    times = read_csv('times.csv')
    print(times)
