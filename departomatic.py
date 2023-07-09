"""departomatic.py

Creates a Windows system tray icon to let you know when to leave for the bus
"""

import sys
import platform
import importlib
import subprocess


def detect_os():
    """
    More friendly OS detection mechanism

    Returns:
        OS: "Windows", "MacOS", "Unknown"
    """
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'MacOS'
    if os_name == 'Windows':
        return 'Windows'

    return 'Unknown'


def main():
    """Main program loop, runs indefinitely
    """
    operating_system = detect_os()
    if operating_system == 'MacOS':
        lib = importlib.import_module('ui.macos')
    elif operating_system == 'Windows':
        lib = importlib.import_module('ui.windows')
    else:
        print("unsupported os")
        sys.exit(1)

    departo = lib.App('./options.yaml', './times.csv')
    departo.run()


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--background':
        main()
    else:
        # Use pythonw to start this script as a background process
        # Pass --background argument to indicate that the script is
        # now running as a background process
        OPERATING_SYSTEM = detect_os()
        if OPERATING_SYSTEM == 'Windows':
            subprocess.Popen(['pythonw', __file__, '--background'])
        elif OPERATING_SYSTEM == 'MacOS':
            subprocess.Popen(['python3', __file__, '--background'])
        else:
            print("unsupported os")
            sys.exit(1)

        # Exit the parent process
        sys.exit(0)
