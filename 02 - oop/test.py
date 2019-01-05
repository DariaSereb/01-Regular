import sys
import scorelib

if __name__ == '__main__':
    if len(sys.argv) !=2:
        print("Wrong number of arguments!")
    else:
        prints = scorelib.load(sys.argv[1])
        for p in prints:
            p.format()
print()
