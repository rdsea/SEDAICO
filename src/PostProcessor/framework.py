#!/usr/bin/env python3

import argparse
import time
from selection import AnnotatedDocumentHandler
from progress.bar import ChargingBar
from util import StatusCodes, bcolors

#static variables
__version__ = "1.0"


if __name__ == '__main__':

    # Define the program description
    text = f'This is a framework program v{__version__}. It can select and present recommendation for the subsystem artefacts, configurations from the artefact repository'

    # Initiate the parser with a description
    parser = argparse.ArgumentParser(description=text)
    parser.add_argument("-V", "--version", version='%(prog)s v{version}'.format(version=__version__), action="version")

    parser.add_argument("-f", "--file", help="Specify the configuration file. Provide full path", default="static/configuration.yml")

    subparsers = parser.add_subparsers(help='Specify mode of operation', dest ="command_type")

    args = parser.parse_args()



    bar = ChargingBar('Initializing framework', max=3)
    for i in range(3):
        time.sleep(0.1)
        bar.next()
    bar.finish()

    # Call appropriate method
    handler = AnnotatedDocumentHandler(args)
    status = handler.validate()
    if status:
        handler.build_recommendations_to_present()
    else:
        print("Failure")
    handler.present_recommendations()
    print(f"{bcolors().WARNING} Completed the work! Exiting")

