"""options.py
Program options loading interface
"""

import yaml


def get_options(file):
    """Load options yaml file

    Args:
        file (str): Path to options.yaml file

    Returns:
        dict: options
    """
    with open(file, 'r', encoding='utf-8') as optionsfile:
        options = yaml.safe_load(optionsfile)

    return options


if __name__ == '__main__':
    opts = get_options('./options.yaml')
    print(opts)
