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

# Map mode args for search method to url query param name for request
SEARCH_MODES = {
    'eq': 'equal',
    'like': 'similar',
    'gt': 'greater',
    'ge': 'greaterequal',
    'lt': 'less',
    'le': 'lessequal'
    }
SEARCH_URL_FORMAT = 'https://distrowatch.com/search.php?pkg={pkg}&relation=' \
    '{mode}&pkgver={ver}&distrorange=InLatest'
RESULTS_XPATH = './body/table[3]/tbody/tr/td[1]/table/tbody/tr[2]/td/table/' \
    'tbody/tr[4]/td/b/a'

def search(package, version, mode='eq'):
    '''Perform a DistroWatch Package Search with given search mode. Searches are
    done only for the latest release of any distro.

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

    mode = SEARCH_MODES[mode]

    package = package.strip().lower()

    if package not in PACKAGE_DICT:
        raise ValueError('Unknown package: "%s"' % package)

    version = version.strip()

    if not version:
        raise ValueError('Version cannot be empty')

    url = SEARCH_URL_FORMAT.format(pkg=package, ver=version, mode=mode)
    charset, data = None, None

    # XXX: this would use strict parsing but html5lib doesn't seem to be able to
    #      handle a DOCTYPE declaration such as:
    #       <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
    #           "http://www.w3.org/TR/html4/loose.dtd">
    parser = html5lib.HTMLParser(namespaceHTMLElements=False)

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

    # Use the XPath to get the list of distro names from the parsed data
    distros = []

    elems = data.findall(RESULTS_XPATH)
    distros = [e.text.strip() for e in elems]

    return distros