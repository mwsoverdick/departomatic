"""times.py
bus stop schedule interface.
"""

import csv
from datetime import datetime, timedelta

def strip_time(string):
    return datetime.strptime(string.strip().replace('a.m.', 'AM').replace(
            'p.m.', 'PM'), '%I:%M %p').time()

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
        stoptimes = [strip_time(row[0]) for row in reader]
    return stoptimes


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


if __name__ == '__main__':
    # usage
    times = read_csv('times.csv')
    print(times)
