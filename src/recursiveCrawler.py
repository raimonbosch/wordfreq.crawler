import abc
from datetime import datetime
from time import sleep
import threading
import requests
from src.crawler import Crawler

class RecursiveCrawler(Crawler):
    def __init__(self, startPage, word, totalThreads):
        super().__init__(startPage, word, totalThreads)

    def startCrawl(self):
        self.crawl(self.startPage, 1, -1, self.pagesCrawled)

    def crawl(self, url, deep, threadNumber, pagesCrawled, elegibleLinks=[]):
        if not self.isCraweable(url, deep, threadNumber):
            return False

        page = requests.get(url)
        elegibleLinks = self.reinforceElegibleLinks(page.text, deep, threadNumber, elegibleLinks, pagesCrawled)
        if len(elegibleLinks) == 0:
            return False

        if self.word in page.text:
            print(f'\n========== Word: {self.word} has been found at {url} (deep: {deep}). Stopping ==========\n')
            self.stopExecution = True
            return False

        if deep == 1:
            self.crawlByThread(elegibleLinks)
        else:
            self.crawl(
                elegibleLinks[0]["href"],
                elegibleLinks[0]["deep"] + 1,
                threadNumber,
                pagesCrawled,
                elegibleLinks[1:self.elegibleLinksSize]
            )

    def crawlByThread(self, elegibleLinks):
        t = 0
        startTime = datetime.now()
        threadList = []
        for link in elegibleLinks[0:self.totalThreads]:
            x = threading.Thread(target=self.crawl, args=(link['href'], 2, t, self.pagesCrawled, []))
            t = t + 1
            x.start()
            sleep(self.politeness / self.totalThreads)
            threadList = threadList + [x]

        for thread in threadList:
            thread.join()

        print(f'Script took {datetime.now() - startTime}')
        print(f'Pages crawled {len(self.pagesCrawled)}')

    @abc.abstractmethod
    def reinforceElegibleLinks(self, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        """Checks if new links must be added to the memory pool of links to crawl"""
        return