#!/usr/bin/env python3
"""
Unit and regression test for the adams_che696_proj package.
"""

# Import package, test suite, and other packages as needed
import sys
import unittest
from contextlib import contextmanager
from io import StringIO
import filecmp
import os

from adams_che696_proj import main


class TestMainFailWell(unittest.TestCase):
#     def testHelp(self):
#         test_input = ['-h']
#         # with capture_stderr(main, test_input) as output:
#         #     self.assertFalse(output)
#         with capture_stdout(main, test_input) as output:
#             self.assertTrue("optional arguments:" in output)
#         # main(test_input)
    def testInvalidScheduler(self):
        test_input = "vmd -e sample.tcl",

class TestMain(unittest.TestCase):
    def testSubmitPBS(self):
        test_input = ["vmd -e sample.tcl", "-j", "tests/quick-job", "-d"]
        try:
            main(test_input)
            with capture_stdout(main, test_input) as output:
                self.assertTrue("qsub" in output)
            self.assertTrue(filecmp.cmp("tests/good_quick-job.pbs", "tests/quick-job.pbs"))
        finally:
            os.remove("tests/quick-job.pbs")

    def testSubmitSlurm(self):
        test_input = ["vmd -e sample.tcl", "-j", "tests/quick-job", "-s", "slurm", "-d"]
        try:
            with capture_stdout(main, test_input) as output:
                self.assertTrue("sbatch" in output)
            self.assertTrue(filecmp.cmp("tests/good_quick-job.job", "tests/quick-job.job"))
        finally:
            os.remove("tests/quick-job.job")


# Utility functions

# From http://schinckel.net/2013/04/15/capture-and-test-sys.stdout-sys.stderr-in-unittest.testcase/
@contextmanager
def capture_stdout(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    out, sys.stdout = sys.stdout, StringIO()
    command(*args, **kwargs)
    sys.stdout.seek(0)
    yield sys.stdout.read()
    sys.stdout = out


def capture_stderr(command, *args, **kwargs):
    # pycharm doesn't know six very well, so ignore the false warning
    # noinspection PyCallingNonCallable
    err, sys.stderr = sys.stderr, six.StringIO()
    command(*args, **kwargs)
    sys.stderr.seek(0)
    yield sys.stderr.read()
    sys.stderr = err

if __name__ == '__main__':
    unittest.main()