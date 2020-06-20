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


    def test_package_invalid_raise(self):
        # Ensure package is a valid value
        with self.assertRaisesRegex(ValueError, 'Unknown package: "foobarfoo"'):
            search('foobarfoo', '1.0')


    def test_version_invalid_raise(self):
        # Ensure it's a non-empty string
        with self.assertRaisesRegex(ValueError, 'Version cannot be empty'):
            search(VALIDPKG, '')
        with self.assertRaisesRegex(ValueError, 'Version cannot be empty'):
            search(VALIDPKG, '\t  ')


if __name__ == '__main__':
    unittest.main()