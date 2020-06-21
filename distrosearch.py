# DistroWatch Distro Package Search
#
# Uses the html5 package to parse the results of Package Search requests
#

from packages import PACKAGES
from urllib.error import URLError
from urllib.request import urlopen
import html5lib

# Keep dict of lowercase package names
PACKAGE_DICT = {p.strip().lower(): p for p in PACKAGES}
SEARCH_MODES = ('eq', 'like', 'gt', 'ge', 'lt', 'le')
SEARCH_URL_FORMAT = ''
RESULTS_XPATH = ''

def search(package, version, mode='eq'):
    '''Perform a DistroWatch Package Search with given search mode.

    Mode defaults to 'eq' and can be any of:
      - eq (equal to)
      - like
      - gt (greater than)
      - ge (greater-or-equal)
      - lt (less than)
      - le (less-or-equal)
    '''

    mode = mode.lower().strip()

    if mode not in SEARCH_MODES:
        raise ValueError('Invalid mode: "%s"' % mode)

    package = package.strip().lower()

    if package not in PACKAGE_DICT:
        raise ValueError('Unknown package: "%s"' % package)

    version = version.strip()

    if not version:
        raise ValueError('Version cannot be empty')

    url = SEARCH_URL_FORMAT.format(pkg=package, ver=version, mode=mode)
    charset, data = None, None

    parser = html5lib.HTMLParser(strict=True)

    # Send the request and get the response data for search results
    try:
        with urlopen(url) as w:
            charset = w.info().get_content_charset()
            data = parser.parse(w, transport_encoding=charset)
    except URLError:
        raise Exception('Error sending search request with url "%s"' % url)
    except html5lib.html5parser.ParseError:
        # ParseError should be raised for badly formed html since parser will be
        # set to strict mode
        raise Exception('Error parsing search response for url "%s"' % url)
