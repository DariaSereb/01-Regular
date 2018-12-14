import sys
import re
from collections import Counter


def search_composers(comp_line):
    line = re.sub('\(.*\)', "", comp_line)
    comp_line = line.split(';')
    results = []
    for composer in comp_line:
        composer = composer.strip()
        if not composer:
            continue
        else:
            results.append(composer)
    return results

def search_centuries(century_line, century_regex, year_regex):

    results = []

    if not century_line:
        return None

    match = re.search(century_regex, century_line)
    if match is not None:
        return match.group(0) + ' century'

    match = re.search(year_regex, century_line)
    if match is not None:
        year = int(match.group(0))
        century = year_to_century(year)
        return century + 'th century'

def main(input, type):

    results = []

    composer_text = 'Composer:'
    century_text = 'Composition Year:'

    century_regex = re.compile('\d\dth')
    year_regex = re.compile('\d\d\d\d')

    with open(input, 'r') as ins:
        if type == 'composer':
            for line in ins:
                if composer_text in line:
                    line = line[len(composer_text):]
                    composers = search_composers(line)
                    results.extend(composers)

        elif type == 'century':
            for line in ins:
                if century_text in line:
                    line = line[len(century_text):].strip()
                    centuries = search_centuries(line, century_regex, year_regex)
                    results.append(centuries)


    results = [r for r in results if r is not None]
    results_counter = Counter(results)
    print_results(results_counter)

def year_to_century(year):
    century = year // 100
    if year % 100 > 0:
        century += 1
    return str(century)

def print_results(results):
    for key in results:
        print("%s: %s" % (key, results[key]))

if __name__ == '__main__':
    input = sys.argv[1]
    type = sys.argv[2]
main(input, type)
