"""departomatic.py

Creates a Windows system tray icon to let you know when to leave for the bus
"""

import sys
import platform
import importlib
import subprocess


def detect_os():
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'MacOS'
    elif os_name == 'Windows':
        return 'Windows'
    else:
        return 'Unknown'


def main():
    """Main program loop, runs indefinitely
    """
    os = detect_os()
    if os == 'MacOS':
        lib = importlib.import_module('ui.macos')
    elif os == 'Windows':
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
        os = detect_os()
        if os == 'Windows':
            subprocess.Popen(['pythonw', __file__, '--background'])
        elif os == 'MacOS':
            subprocess.Popen(['python3', __file__, '--background'])
        else:
            print("unsupported os")
            sys.exit(1)

        # Exit the parent process
        sys.exit(0)
