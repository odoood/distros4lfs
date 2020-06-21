# Unit tests for distrosearch module

import sys
sys.path.append('..')

from pathlib import Path
import distrosearch
from distrosearch import search
import unittest

SCRIPTDIR = Path(sys.argv[0]).parent

if not SCRIPTDIR.is_absolute():
    SCRIPTDIR = SCRIPTDIR.resolve()

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


    def test_request_fails_raise(self):
        # If request to DistroWatch fails show error message indicating that
        # Set the url format for requests to force failure
        s = distrosearch.SEARCH_URL_FORMAT
        distrosearch.SEARCH_URL_FORMAT = (SCRIPTDIR / 'foobar.txt').as_uri()

        with self.assertRaisesRegex(Exception, 'Error sending search request'):
            search(VALIDPKG, '1.0')

        distrosearch.SEARCH_URL_FORMAT = s


if __name__ == '__main__':
    unittest.main()