"""options.py
Program options loading interface.

Handles any quirks with loading/parsing options.yaml.
"""

import yaml
from .times import strip_time


def get_options(file):
    """Load options yaml file

    Args:
        file (str): Path to options.yaml file

    Returns:
        dict: options
    """
    with open(file, 'r', encoding='utf-8') as optionsfile:
        options = yaml.safe_load(optionsfile)

    return __sanitize(options)


def __sanitize(options: dict):
    """
    Sanitize options dict before returning.

    Initialize missing options.
    Convert options to more useful types.

    Args:
        options: options dict
    """

    options = __sanitize_annoy(options)
    return options


def __sanitize_annoy(options):
    """
    Ininitializes/Sanitizes annoy options to comply with class behaviors
    """

    # Default behavior is to not be annoying
    if "annoy" not in options:
        options["annoy"] = {
                "enable": False
        }

    # If unbounded, the default is to annoy 24/7
    if "start" in options["annoy"] and "stop" in options["annoy"]:
        options["annoy"]["start"] = strip_time(options["annoy"]["start"])
        options["annoy"]["stop"] = strip_time(options["annoy"]["stop"])
    else:
        options["annoy"]["start"] = None
        options["annoy"]["stop"] = None

    # If not specified, the annoy rate is every minute
    if "rate" not in options["annoy"]:
        options["annoy"]["rate"] = 1

    return options

# Quick test to see that options load as expected
if __name__ == '__main__':
    opts = get_options('../options.yaml')
    print(opts)
