from PageExtractor import PageExtractor, ExtractorConfiguration

import re
import argparse

parser = argparse.ArgumentParser(
    description='Extracts wordlist from websites.')
parser.add_argument('--start_url', metavar='start_url', type=str,
                    help='The url we will start the crawling from.')
parser.add_argument('--url_prefix', metavar='url_prefix', type=str,
                    help='The prefix we look for in the links.')
parser.add_argument('--regex', metavar='regex', type=str,
                    help='The regex you want links to match')
parser.add_argument('--depth', metavar='depth', type=int,
                    help='The depth of the crawling process.')
parser.add_argument('--output', metavar='output', default="result.txt", type=str,
                    help='Name of output file')
parser.add_argument('-v', action='store_true', help='Verbose')

args = parser.parse_args()
params = vars(args)
if not params['start_url']:
    params['start_url'] = input(
        "Enter the url you want to start the crawling from: ")
if not params['url_prefix'] and not params['regex']:
    if(input("Type 'r' if you want to enter a regex for the links or any other character if you want to enter a url prefix.") == 'r'):
        params['url_prefix'] = input("Enter the prefix we look for in the links: ")
    else:
        params['regex'] = input("Enter regex we look for in the links: ")
if not params['depth']:
    params['depth'] = int(input("Enter crawling depth: "))
if not params['output']:
    params['output'] = int(input("Enter name of output file: "))

pg: PageExtractor = PageExtractor(
    params['start_url'], ExtractorConfiguration(depth=params['depth'], verbose=params['v']))

pg.load_page()

if params['regex'] is not None:
    pg.filter_links(lambda x: re.search(params['regex'], x))
else:
    pg.filter_links(lambda x: x.startswith(params['url_prefix']))

pg.traverse_all_links()

print("Extracted " + str(len(pg.words)) + " words!")
with open(params['output'], 'w') as f:
    for item in pg.get_words():
        f.write("%s\n" % item)
