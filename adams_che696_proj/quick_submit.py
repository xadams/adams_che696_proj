#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
quick_submit.py
Class project that submits a single line of commands to a cluster

Handles the primary functions
"""

import sys
import argparse
import subprocess

TYPES = ["pbs", "slurm"]
DEF_TYPE = ["pbs"]


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser(description="Submit a single line of commands to a scheduler.")
    parser.add_argument('command', metavar="command", type=str)
    # parser.add_argument("-c", "--command", help="The single line to be submitted", type=str)
    parser.add_argument("-s", "--scheduler", help="The scheduler available on this cluster. Valid options are {}. "
                                                  " The default option is {}.".format(TYPES, DEF_TYPE), choices=TYPES,
                        default=DEF_TYPE)
    args = None
    try:
        args = parser.parse_args(argv)
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, 2

    return args, 0


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != 0:
        return ret
    print(args.command)
    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
