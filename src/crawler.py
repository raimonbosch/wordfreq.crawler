import abc
import re
from datetime import datetime
import requests
from time import sleep
import threading
from src.linkHelper import LinkHelper

class Crawler:
    def __init__(self, startPage, word, totalThreads):
        self.pagesCrawled = []
        self.startPage = startPage
        self.homePage = re.sub(r'(http(s)?://[^/]+/)(.*)', r'\1', startPage)
        if not self.homePage.endswith('/'):
            self.homePage = self.homePage + '/'
        self.linkHelper = LinkHelper(self.homePage)
        self.word = word
        self.totalThreads = totalThreads
        self.politeness = 0.005
        self.elegibleLinksSize = 100
        self.debug = False
        self.stopExecution = False

    def isCraweable(self, url, deep, threadNumber):
        if self.stopExecution:
            return False

        if deep > 100:
            return False

        print(f'\nCawling url {url}; deep:{deep}; thread:{threadNumber};')
        sleep(self.politeness)
        self.pagesCrawled += [url]

        return True

    def startCrawl(self):
        """Defines how to start to crawl"""
        return

    def crawl(self, url, deep, threadNumber, pagesCrawled, elegibleLinks = []):
        """Defines crawl strategy to follow"""
        return

    @abc.abstractmethod
    def reinforceElegibleLinks(self, url, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        """Checks if new links must be added to the memory pool of links to crawl"""
        return