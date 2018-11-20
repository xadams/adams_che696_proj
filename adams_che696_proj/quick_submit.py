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
import re
from shutil import which

TYPES = ["pbs", "slurm"]

## Default Values
DEF_TYPE = "pbs"
DEF_PROCS = 1
DEF_MEM = 4
DEF_NAME = "quick-job"
DEF_TIME = 1
DEF_PATH = "/Users/xadams/PycharmProjects/adams_che696_proj/adams_che696_proj/data/"

## Dictionary Keywords
WALLTIME = 'walltime'
NUM_PROCS = 'num_procs'
MEM = 'mem'
JOB_NAME = 'job_name'


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


def proc_args(keys):
    tpl_vals = {}

    tpl_vals[WALLTIME] = keys.walltime
    tpl_vals[NUM_PROCS] = keys.num_procs
    tpl_vals[MEM] = keys.memory
    tpl_vals[JOB_NAME] = keys.job_name

    return tpl_vals


def make_jobfile(cfg, vals):
    if cfg.scheduler == "pbs":
        tpl = cfg.path + "template.pbs"
        fout_name = "./" + cfg.job_name + ".pbs"
    elif cfg.scheduler == "slurm":
        tpl = cfg.path + "template.job"
        fout_name = "./" + cfg.job_name + ".job"


    with open(fout_name, 'w') as fout:
        with open(tpl, 'rt') as fin:
            for line in fin:
                if '{' in line:
                    key = re.search('{(.*)}', line)
                    for kw in vals:
                        if kw == key.group(1):
                            fout.write(line.replace("{"+kw+"}", str(vals[kw])))
                else:
                    fout.write(line)
        fout.write(cfg.command)

    return fout_name

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
    parser.add_argument("-n", "--num_procs", help="Number of processors requested. Default is {}.".format(DEF_PROCS),
                        default=DEF_PROCS)
    parser.add_argument("-m", "--memory", help="Memory per node, as integer. Default is {} (gb).".format(DEF_MEM),
                        type=int, default=DEF_MEM)
    parser.add_argument("-j", "--job_name", help="Name for the submitted job. Default is {}.".format(DEF_NAME),
                        type=str, default=DEF_NAME)
    parser.add_argument("-w", "--walltime", help="Time in hours for the submitted job. "
                                                 "Default is {} (hr).".format(DEF_TIME), type=int, default=DEF_TIME)
    parser.add_argument("-p", "--path", help="Path to template file", default=DEF_PATH)
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
    tpl_vals = proc_args(args)
    submit_name = make_jobfile(args, tpl_vals)
    if args.scheduler == "pbs":
        if which('qsub'):
            subprocess.call(['qsub', submit_name])
        else:
            print("qsub {}".format(submit_name))
    elif args.scheduler == "slurm":
        if which('sbatch'):
            subprocess.call(['sbatch', submit_name])
        else:
            print("sbatch {}".format(submit_name))
    return 0  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
