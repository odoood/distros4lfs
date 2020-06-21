# Use distrowatch module to compile list of distros that fulfill the LFS host
# system package reqirements
import distrosearch
from pathlib import Path
import sys

filedir = Path(sys.argv[0]).parent.resolve()
LFSPKG_FILE = filedir / 'lfspkglist.txt'
DISTRO_FILE = filedir / 'distrolist.txt'

if not LFSPKG_FILE.exists():
    print('Package list file missing: "%s"' % LFSPKG_FILE)
    exit(1)

package_map = {}

# Read all the lines in the package list - the format should be:
# PackageName   PackageVersion  SearchMode
# With SearchMode value according to accepted distrosearch.search mode arg
package_list = []

with open(LFSPKG_FILE) as pf:
    for pkg in pf:
        package_list.append(pkg.strip().split())

print('List of packages to search for:')
print('\n'.join([pkg[0] + ' ' + pkg[2] for pkg in package_list]))

# Do the search for all packages and add the list of results to the map
print('\nPerforming package searches...\n')

for (name, mode, version) in package_list:
    print('Searching for distros with "%s %s"...' % (name, version))
    key = '%s (%s %s)' % (name, mode, version)
    package_map[key] = distrosearch.search(name, version, mode)

print('\nPackages (and number of qualifying distros):\n')

for pkg in sorted(package_map.keys()):
    print('{: <20}: {}'.format(pkg, len(package_map[pkg])))

# Get set of distros which comply with all host requirements
good_distros = set()
bad_distros = set()
distro_sets = list(filter(None, package_map.values()))

# Check each distro in each list and ensure it's in all the other lists
for distro_set in distro_sets:
    for distro in distro_set:
        if distro in good_distros or distro in bad_distros:
            continue

        # Add to the bad set at first set where it's not found, else the good 
        for ds in distro_sets:
            if distro not in ds:
                bad_distros.add(distro)
                break
        else:
            good_distros.add(distro)

# Print out the good distros for LFS host systems if any
if len(good_distros) == 0:
    print('\nNo candidates found.')
    exit(0)

print('\nHost system candidates:\n%s\n' % '\n'.join(sorted(good_distros)))

with open(DISTRO_FILE, 'w') as df:
    df.write('Distros which meet all the following requirements:\n\n')

    for p in package_map:
        df.write('- %s\n' % p)

    df.write('\n%s' % '\n'.join(sorted(good_distros)))

print('List written to "%s"' % DISTRO_FILE)