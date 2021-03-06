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

# Context manager method for setting the RESULTS_XPATH in module
@contextmanager
def xpath_context(path):
    p = distrosearch.RESULTS_XPATH
    distrosearch.RESULTS_XPATH = path
    try:
        yield
    finally:
        distrosearch.RESULTS_XPATH = p


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

    # FIXME: need an easy way to force parsing failure without using strict mode
    @unittest.skip('Cannot fail with strict=False?')
    def test_parsing_fails_raise(self):
        # If request succeeds but parsing the html data fails show error for it
        # Use url format context for request to force load dummy file
        url = (DUMMY_FILE_DIR / 'badhtml.html').as_uri()
        errormsg = 'Error parsing search response for url "%s"' % url

        with self.assertRaisesRegex(Exception, errormsg):
            with url_context(url):
                search(VALIDPKG, '1.0')


    def test_no_search_results_return_empty_list(self):
        url = (DUMMY_FILE_DIR / 'noresults.html').as_uri()

        with url_context(url), xpath_context(''):
            result = search(VALIDPKG, '1.0')
            self.assertEqual([], result)


    def test_one_result_return_list_of_one(self):
        url = (DUMMY_FILE_DIR / 'oneresult.html').as_uri()
        xp = "./body/div[@id='search-results']/ul/li"

        with url_context(url), xpath_context(xp):
            result = search(VALIDPKG, '1.0')
            self.assertEqual(['The Only One'], result)


    def test_three_results_return_list_of_three(self):
        url = (DUMMY_FILE_DIR / 'threeresults.html').as_uri()
        xp = "./body/div[@id='search-results']/ul/li"
        expected = ['The First', 'The   2nd: Number Two', 'Third Result']

        with url_context(url), xpath_context(xp):
            result = search(VALIDPKG, '1.0')
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
