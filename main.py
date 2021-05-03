import argparse
from logger import logger
from wiki_utils import WikiUtils

"""Wiki Link-Back
A computer program that receives a URL to a
Wikipedia article on the command line.  The program will print a list of URLs
to other Wikipedia articles that are linked to from the original article, and
also link back to it.
"""


def get_URL():
    """:returns the url from the program arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str)
    return parser.parse_args().url


def main():
    try:
        logger.info("Start running...")
        original_URL = get_URL()
        if not WikiUtils.is_wiki_page(original_URL):
            raise Exception("Incorrect Input.")
        wiki_links = WikiUtils.get_wiki_links(original_URL)
        page_name = original_URL.split(r'/')[-1]
        logger.info(f"Total number of Wikipedia links is the page '{page_name}' - {len(wiki_links)}")
        WikiUtils.print_wiki_back_links(original_URL, wiki_links)

    except Exception as e:
        logger.exception(e)


if __name__ == "__main__":
    main()


