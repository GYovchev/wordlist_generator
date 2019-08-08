import requests
import re

from bs4 import BeautifulSoup
import lxml


class ExtractorConfiguration():
    def __init__(self, depth=0, verbose=True):
        self.verbose = verbose
        self.depth = depth

    def create_configuration_with_decreased_depth(self):
        return ExtractorConfiguration(self.depth-1)


class PageExtractor():
    def __init__(self, url: str, config: ExtractorConfiguration):
        self.url = url
        self.config = config
        self.links = set()
        self.words = set()
        self.filters = []

    def load_page(self):
        """ Method that loads all words into `self.words` set and all links that could be potential pages we want to scrape. """
        page_response = requests.get(self.url)
        html = page_response.text
        parsed = BeautifulSoup(html, "html.parser")

        # Remove tags that need source code as content
        for script in parsed(["script", "style"]):
            script.extract()

        for link in parsed.findAll('a', attrs={'href': re.compile("^https{0,1}://")}):
            self.links.add(link.get('href'))

        # Get the text and remove extra whitespaces
        text = parsed.get_text()
        text = re.sub('\s+', ' ', text).strip()

        # Get all words and fiter them. We use \w because we want that code to work for many languages
        words = re.findall(r"\b(\w{1,})\b", text)
        words = list(filter(lambda x: any(x.islower() for i in x), words))

        # Add every word to the set
        for word in words:
            self.words.add(word)

    def filter_links(self, link_filter):
        """ Filters all links usint custom function. It takes one paramter - the link and
            if it returns 0 or False the element is removed from the set """
        self.filters.append(link_filter)
        self.links = set(filter(link_filter, self.links))

    def traverse_all_links(self, depth=None):
        if depth is None:
            depth = self.config.depth
        if(depth == 0):
            return
        self._l("To extract " + str(len(self.links)) + " urls")
        extracted = 0
        for link in self.links:
            pg = PageExtractor(
                link, self.config.create_configuration_with_decreased_depth())
            pg.load_page()
            for filter in self.filters:
                pg.filter_links(filter)
            pg.traverse_all_links()
            self._merge_words(pg)
            extracted = extracted + 1
            self._l("Extracted " + str(extracted) +
                  "/" + str(len(self.links)) + " urls")

    def get_words(self):
        return self.words

    def _merge_words(self, pg):
        self.words = self.words | pg.get_words()
    
    def _l(self, s):
        if self.config.verbose:
            print(s)
