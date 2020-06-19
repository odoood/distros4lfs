# Unit tests for distrosearch module

import sys
sys.path.append('..')

from distrosearch import search
import unittest

VALIDPKG = 'linux'

class SearchTests(unittest.TestCase):

    def test_mode_invalid_raise(self):
        # Ensure mode is a valid value
        with self.assertRaisesRegex(ValueError, 'Invalid mode: "badmode"'):
            search(VALIDPKG, '1.0', 'badmode')


if __name__ == '__main__':
    unittest.main()