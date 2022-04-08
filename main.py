import sys

from src.simpleCrawler import SimpleCrawler
from src.zipfCrawler import ZipfCrawler

if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) >= 1:
        homePage = args[0]
    else:
        homePage = 'https://es.wikipedia.org/'

    if len(args) >= 2:
        word = args[1]
    else:
        word = 'Tenerife'

    if len(args) >= 3:
        language = args[2]
    else:
        language = 'es'

    if len(args) >= 4:
        numThreads = int(args[3])
    else:
        numThreads = 1

    crawler = ZipfCrawler(homePage, word, numThreads, language)
    crawler.startCrawl()
