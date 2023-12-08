import getopt
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

def debug_print(s):
    if verboseMode:
        print(s)
    else:
        pass
        
# Default configuration
filename = None # results file name
search_phrase = None
verboseMode = False
results_count = 10

# Parsing arguments
argumentsList = sys.argv[1:]

options = "hs:f:c:v"

long_options = ["search=", "file=", "count=", "help", "verbose"]

try:
    arguments, values = getopt.getopt(argumentsList, options, long_options) 
    
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("scraper: scrapes wikipedia for fun")
            print('''
            Options:
            -s, --search: specifies the search phrase
            -f, --file: redirects the output to a file
            -c, --count: specifies how many results will be saved 
            (only works with -f)
            -v, --verbose: verbose output
            -h, --help: shows this window
            ''')

        if current_argument in ("-s", "--search"):
           search_phrase = current_value 

        if current_argument in ("-f", "--file"):
            filename = current_value

        if current_argument in ("-c", "--count"):
            results_count = int(current_value)

        if current_argument in ("-v", "--verbose"):
            verboseMode = True
    debug_print(f"Options: {arguments}")
    
except getopt.error as err:
    print(str(err))
    sys.exit("\nUse -h for more info")

if search_phrase is None:
    sys.exit("Execution failed: No search phrase specified")
    
search_phrase = search_phrase.replace(" ", "+")
search_phrase = search_phrase.replace("-", "+")
url = f"https://en.wikipedia.org/w/index.php?fulltext=1&search={search_phrase}&title=Special%3ASearch&ns0=1"
debug_print(f'URL: {url}')
raw_html = urlopen(url).read()
html = soup(raw_html, "html.parser")
html.prettify()

    
if filename is not None:
    titles = html.find_all("div", {"class": "mw-search-result-heading"}, limit=results_count)
    descriptions = html.find_all("div", {"class": "searchresult"}, limit=results_count)
    delimiter = '-'*40
    with open(filename, "w") as f:
        for t, d in zip(titles, descriptions):
            f.write(f"{t.get_text()}\n{d.get_text()}\n{delimiter}\n")

else:
    title = html.find("div", {"class": "mw-search-result-heading"})
    description = html.find("div", {"class": "searchresult"})
    print(f"{title.get_text()}\n{description.get_text()}")
