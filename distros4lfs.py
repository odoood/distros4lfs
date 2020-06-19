# From a text list of distros (compiled from distrowatch.com search for distros
# by package) get the set of distros that fulfill the LFS host system reqs
from pathlib import Path
import sys

filedir = Path(sys.argv[0]).parent
distro_file = filedir / 'distros4lfs.txt'
package_map = {}

# Read all the lines in the list - the format should be:
# PackageName\t[list of distros with tab delim]
with open(distro_file) as df:

    # Add the list of distros to the package map with the package as key
    for pkg in df:

        line = pkg.strip().split('\t')
        package_map[line[0]] = set(line[1:])

print('Packages (and number of qualifying distros):')

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

# Print out the good distros for LFS host systems
print()
print('Host system candidates (caveat: need to be checked for the packages -> {}):'
      .format(', '.join([p for p in package_map if not package_map[p]])))

for d in sorted(good_distros):
    print(d)

        
        
