from bs4 import BeautifulSoup

from src.recursiveCrawler import RecursiveCrawler
from src.wordFrequencyHelper import WordFrequencyHelper

class SemanticCrawler(RecursiveCrawler):
    def __init__(self, homePage, word, totalThreads, language):
        self.wordFreqHelper = WordFrequencyHelper(language)
        self.wordScore = self.wordFreqHelper.getWordFrequency(word)
        super().__init__(homePage, word, totalThreads)
        print(f'Word: {self.word}; Score: {self.wordScore}; language: {language}')
        self.debug = True

    def reinforceElegibleLinks(self, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        for link in BeautifulSoup(htmlText, 'html.parser').find_all('a'):
            link["score"] = self.wordFreqHelper.getAnchorWordFrequency(link.text)
            link["deep"] = deep
            if self.linkHelper.linkElegible(link, elegibleLinks, pagesCrawled):
                elegibleLinks += [link]

        elegibleLinks.sort(key=self.sortElegibleLinks)
        elegibleLinks = elegibleLinks[0:self.elegibleLinksSize]

        if self.debug:
            self.printElegibleLinks(elegibleLinks, threadNumber)

        return elegibleLinks

    def sortElegibleLinks(self, link):
        if link["deep"] > 10:
            return 100000

        return abs(self.wordScore - link["score"])

    def printElegibleLinks(self, elegibleLinks, threadNumber):
        i = 0
        for link in elegibleLinks:
            i = i + 1
            print(f'{threadNumber}|{i}.- {link["href"]}; {link.text}; deep:{link["deep"]}; score:{link["score"]}')