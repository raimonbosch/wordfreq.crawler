from bs4 import BeautifulSoup
from src.recursiveCrawler import RecursiveCrawler

class SimpleCrawler(RecursiveCrawler):
    def __init__(self, startPage, word, totalThreads):
        super().__init__(startPage, word, totalThreads)

    def reinforceElegibleLinks(self, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        elegibleLinks = [] #In this case we always clean up links
        for link in BeautifulSoup(htmlText, 'html.parser').find_all('a'):
            link["deep"] = deep
            if self.linkHelper.linkElegible(link, elegibleLinks, pagesCrawled):
                elegibleLinks += [link]

        elegibleLinks = elegibleLinks[0:self.elegibleLinksSize]

        if self.debug:
            i = 0
            for link in elegibleLinks:
                i = i + 1
                print(f'{threadNumber}|{i}.- {link["href"]}; {link.text}; deep:{link["deep"]};')

        return elegibleLinks