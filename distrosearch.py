# DistroWatch Distro Package Search
#
# Uses the html5 package to parse the results of Package Search requests
#

SEARCH_MODES = ('eq', 'like', 'gt', 'ge', 'lt', 'le')

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

