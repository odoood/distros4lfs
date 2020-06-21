# Unit tests for distrosearch module

import sys
import unittest
from pathlib import Path
from contextlib import contextmanager

sys.path.append('..')

import distrosearch
from distrosearch import search

SCRIPTDIR = Path(sys.argv[0]).parent

if not SCRIPTDIR.is_absolute():
    SCRIPTDIR = SCRIPTDIR.resolve()

DUMMY_FILE_DIR = SCRIPTDIR / 'dummy_files'

VALIDPKG = 'linux'

# Context manager method for setting the SEARCH_URL_FORM in target module
@contextmanager
def url_context(url):
    s = distrosearch.SEARCH_URL_FORMAT
    distrosearch.SEARCH_URL_FORMAT = url
    try:
        yield
    finally:
        distrosearch.SEARCH_URL_FORMAT = s


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
        # Use url format context for requests to force failure
        url = (SCRIPTDIR / 'foobar.txt').as_uri()
        errormsg = 'Error sending search request with url "%s"' % url

        with self.assertRaisesRegex(Exception, errormsg):
            with url_context(url):
                search(VALIDPKG, '1.0')


    def test_parsing_fails_raise(self):
        # If request succeeds but parsing the html data fails show error for it
        # Use url format context for request to force load dummy file
        url = (DUMMY_FILE_DIR / 'badhtml.html').as_uri()
        errormsg = 'Error parsing search response for url "%s"' % url

        with self.assertRaisesRegex(Exception, errormsg):
            with url_context(url):
                search(VALIDPKG, '1.0')



if __name__ == '__main__':
    unittest.main()
