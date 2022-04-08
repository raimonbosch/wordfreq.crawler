
class LinkHelper:
    def __init__(self, homePage):
        self.homePage = homePage
        self.imageFormats = [".jpg", ".svg", ".ogg", ".png"]

    def linkElegible(self, link, elegibleLinks, newElegibleLinks, pagesCrawled, url):
        if not self.linkFormatIsCorrect(link):
            return False

        link = self.transformToAbsoluteLinks(link)

        if link['href'] == url:
            return False

        if self.homePage not in link['href']:
            return False

        if link['href'] in pagesCrawled:
            return False

        for newElegibleLink in newElegibleLinks:
            if newElegibleLink['href'] == link['href']:
                return False

        for elegibleLink in elegibleLinks:
            if elegibleLink['href'] == link['href']:
                return False

        return True

    def linkFormatIsCorrect(self, link):
        if 'href' not in link.attrs:
            return False

        if '#' in link['href']:
            return False

        if '?' in link['href']:
            return False

        for imageFormat in self.imageFormats:
            if link['href'].endswith(imageFormat):
                return False

        return True

    def transformToAbsoluteLinks(self, link):
        if link['href'].startswith('//'):
            link['href'] = link['href'].replace('//', 'https://')

        if link['href'].startswith('/'):
            link['href'] = link['href'].replace('/', self.homePage, 1)

        return link