import sys
import scorelib


def load(filename):
    filename = sys.argv[1]
    prints = scorelib.load(filename)
    
    for line in prints:
        line.format()
        print('')


