# DistroWatch Distro Package Search
#
# Uses the html5 package to parse the results of Package Search requests
#

from packages import PACKAGES

SEARCH_MODES = ('eq', 'like', 'gt', 'ge', 'lt', 'le')

# Keep dict of lowercase package names
PACKAGE_DICT = {p.strip().lower(): p for p in PACKAGES}

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