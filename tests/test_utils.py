import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(
                             inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import utils.utils as utils

from nose.tools import assert_equals


class TestUtils:
    # Test util methods

    def test_execute_shell(self):
        out, err = utils.execute_shell('echo hello')
        assert_equals(out, "hello\n")
