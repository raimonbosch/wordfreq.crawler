import abc
from datetime import datetime
from email import header
from time import sleep
import threading
import requests
from src.crawler import Crawler

class IterativeCrawler(Crawler):
    def __init__(self, startPage, word, totalThreads):
        super().__init__(startPage, word, totalThreads)

    def startCrawl(self):
        self.crawlByThread(
            self.crawl(self.startPage, 1, -1, self.pagesCrawled)
        )

    def crawl(self, url, deep, threadNumber, pagesCrawled, elegibleLinks = []):
        if not self.isCraweable(url, deep, threadNumber):
            return False

        myHeader = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/W.X.Y.Z Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
        }
        page = requests.get(url, headers=myHeader)
        elegibleLinks = self.reinforceElegibleLinks(url, page.text, deep, threadNumber, elegibleLinks, pagesCrawled)
        if len(elegibleLinks) == 0:
            return False

        if self.word in page.text:
            print(f'\n========== Word: {self.word} has been found at {url} (deep: {deep}). Stopping ==========\n')
            self.stopExecution = True
            return True

        return elegibleLinks

    def crawlByThread(self, elegibleLinks):
        t = 0
        startTime = datetime.now()
        threadList = []
        for link in elegibleLinks[0:self.totalThreads]:
            x = threading.Thread(
                target=self.crawlWaitingList,
                args=(list(dict.fromkeys([link] + elegibleLinks)), t)
            )
            t = t + 1
            x.start()
            sleep(self.politeness/self.totalThreads)
            threadList = threadList + [x]

        for thread in threadList:
            thread.join()

        print(f'Script took {datetime.now() - startTime}')
        print(f'Pages crawled {len(self.pagesCrawled)}')

    def crawlWaitingList(self, elegibleLinks, threadNumber):
        while True:
            elegibleLinks = self.crawl(
                elegibleLinks[0]['href'],
                elegibleLinks[0]['deep'] + 1,
                threadNumber,
                self.pagesCrawled,
                elegibleLinks
            )

            if elegibleLinks == False:
                return False

            if elegibleLinks == True:
                return True

    @abc.abstractmethod
    def reinforceElegibleLinks(self, url, htmlText, deep, threadNumber, elegibleLinks, pagesCrawled):
        """Checks if new links must be added to the memory pool of links to crawl"""
        return