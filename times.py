import csv
from datetime import datetime


def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header
        data = [datetime.strptime(row[0].strip().replace('a.m.', 'AM').replace(
            'p.m.', 'PM'), '%I:%M %p').time() for row in reader]
    return data


if __name__ == '__main__':
    # usage
    data = read_csv('times.csv')
    print(data)
