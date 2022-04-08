from wordfreq import zipf_frequency, word_frequency
from urllib.parse import unquote
import unidecode
import re

class WordFrequencyHelper:
    def __init__(self, language):
        self.language = language

    def getZipfFromWord(self, word):
        return zipf_frequency(word, self.language)

    def getWordFrequency(self, word):
        return word_frequency(word, self.language)

    def getAnchorWordFrequency(self, anchorWord):
        median = 0
        parts = anchorWord.split(' ')
        for part in parts:
            median += word_frequency(part, self.language)

        if len(parts) > 0:
            median = median / len(parts)

        return median

    def getZipf(self, anchor):
        median = 0
        parts = anchor.split(' ')
        for part in parts:
            median += zipf_frequency(part, self.language)

        if len(parts) > 0:
            median = median / len(parts)

        return median

    def getUrlScore(self, url, homePage):
        #url decode
        urlClean = unquote(url).replace(homePage, '')
        #remove home and language tags
        urlClean = urlClean.replace(homePage, '').replace(self.language + "/", '')
        #remove accents
        urlClean = unidecode.unidecode(urlClean)
        anchorLink = ' '.join(re.findall("[a-zA-Z0-9]+", urlClean))

        return self.getZipf(anchorLink)