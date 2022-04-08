from bs4 import BeautifulSoup

from src.iterativeCrawler import IterativeCrawler
from src.wordFrequencyHelper import WordFrequencyHelper

class ZipfCrawler(IterativeCrawler):
    def __init__(self, homePage, word, totalThreads, language):
        self.zipfHelper = WordFrequencyHelper(language)
        self.language = language
        self.zipWordScore = self.zipfHelper.getZipfFromWord(word)
        super().__init__(homePage, word, totalThreads)
        print(f'Word: {self.word}; Score: {self.zipWordScore}; language: {language}')
        self.debug = False
        self.elegibleLinksSize = 30

    def reinforceElegibleLinks(self, url, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        newElegibleLinks = []

        for link in elegibleLinks:
            if not self.linkHelper.linkElegible(link, [], [], self.pagesCrawled, url):
                elegibleLinks.remove(link)

        for link in BeautifulSoup(htmlText, 'html.parser').find_all('a'):
            link["score"] = self.zipfHelper.getZipf(link.text)
            link["parentUrl"] = url
            link["thread"] = threadNumber

            if deep >= 7:
                link["deep"] = 1
            else:
                link["deep"] = deep

            if self.linkHelper.linkElegible(link, elegibleLinks, newElegibleLinks, self.pagesCrawled, url):
                newElegibleLinks += [link]

        newElegibleLinks.sort(key=self.sortElegibleLinks)
        if deep > 1:
            newElegibleLinks = newElegibleLinks[0:5]

        for newLink in newElegibleLinks:
            if newLink not in elegibleLinks:
                elegibleLinks = elegibleLinks + [newLink]

        elegibleLinks.sort(key=self.sortElegibleLinks)
        elegibleLinks = elegibleLinks[0:self.elegibleLinksSize]

        #Cleaning up elegible links when we are in deep == 6
        for url in self.pagesCrawled:
            for link in elegibleLinks:
                if link['href'] == url:
                    elegibleLinks.remove(link)

        if self.debug:
            self.printElegibleLinks(url, elegibleLinks, threadNumber, deep)

        return elegibleLinks

    def sortElegibleLinks(self, link):
        if link["deep"] > 1 and link["deep"] <= 4:
            score = abs(5 + 0.05*link["thread"] - link["score"])
        else:
            score = abs(self.zipWordScore + 0.05*link["thread"] - link["score"])
        #score = abs(self.zipWordScore + 0.05 * link["thread"] - link["score"])

        if f'/{self.language}/' in link['href'] or f'https://{self.language}.' in link['href']:
            score = score / 1000

        if link['href'] in self.pagesCrawled:
            score = 10000000

        return score

    def printElegibleLinks(self, url, elegibleLinks, threadNumber, deep):
        i = 0
        score = 0
        for link in elegibleLinks:
            i = i + 1
            score = score + link["score"]
            print(f'{threadNumber}|{i}.- {link["href"]}; {link.text.strip()}; deep:{link["deep"]}; score:{link["score"]}; parentUrl:{link["parentUrl"]};')

        if i > 0:
            score = score / i
            print(f'url: {url}; deep: {deep}; Score median: {score};')