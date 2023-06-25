# simple debug utilities
import argparse

verbose = False

def setup_debug():
    global verbose
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    args = parser.parse_args()

    verbose = args.verbose

def debug(to_print):
    if verbose:
        print(to_print)