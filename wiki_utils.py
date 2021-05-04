import re
from urllib import request
from concurrent.futures import ThreadPoolExecutor, as_completed

class WikiUtils:
    """A class which contains all the needed utilities to get and parse a Wikipedia page"""

    BASE_WIKI_URL = "https://en.wikipedia.org"
    """English Wikipedia's URLs begin https://en.wikipedia.org/. 
    That address on its own is redirected to the Main Page. The main form of a URL to a Wikipedia page: 
    https://en.wikipedia.org/wiki/Page_name (from - Wikipedia, Help:URL)
    """

    @staticmethod
    def is_wiki_page(URL):
        """:returns True if the page is an absolute or a relative Wikipedia page"""
        if URL.startswith("/wiki/"):
            URL = WikiUtils.BASE_WIKI_URL + URL
        try:
            web_URL = request.urlopen(URL)
        except Exception:
            return False
        return web_URL.getcode() == 200 and URL.startswith(WikiUtils.BASE_WIKI_URL)

    @staticmethod
    def full_wiki_URL(URL):
        """:returns absolute url, assuming that the input is a Wikipedia page URL"""
        return (WikiUtils.BASE_WIKI_URL + URL) if URL.startswith("/wiki/") else URL

    @staticmethod
    def get_links(URL):
        """:returns all the links in the html page using regex"""
        website = request.urlopen(URL)
        html = website.read().decode()
        return list(set(re.findall(r'href=[\'"]?([^\'" >]+)', html)))

    @staticmethod
    def get_wiki_links(URL):
        """:return all the Wikipedia links in the html page"""
        files = list(filter(WikiUtils.is_wiki_page, WikiUtils.get_links(URL)))
        return files

    @staticmethod
    def get_relative_wiki_URL(URL):
        """:returns the relative path, assuming that the input is a Wikipedia page"""
        return URL.replace(WikiUtils.BASE_WIKI_URL, "")

    @staticmethod
    def print_back_link(original_URL, URL):
        """print URL if it links to original_URL"""
        URL = WikiUtils.full_wiki_URL(URL)
        if URL == original_URL:
            return
        links = WikiUtils.get_links(URL)
        original_relative_URL = WikiUtils.get_relative_wiki_URL(original_URL)
        if original_URL in links or original_relative_URL in links:
            print(URL)

    @staticmethod
    def print_wiki_back_links(original_URL, URLs):
        print("*"*20, "\nBack Links:")
        with ThreadPoolExecutor() as executor:
            futures = []
            for URL in URLs:
                futures.append(executor.submit(WikiUtils.print_back_link, original_URL=original_URL, URL=URL))

            as_completed(futures)

        print("*"*20)









