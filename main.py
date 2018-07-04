import time
import urllib

import requests
from bs4 import BeautifulSoup


def continue_crawl(search_history, target_url):
    if search_history[-1] == target_url:
        return False
    if len(search_history) > 25:
        return False
    i = 0
    while(i < len(search_history)):
        j = i+1
        while(j < len(search_history)):
            if search_history[i] == search_history[j]:
                return False
            j += 1
        i += 1
    return True

def find_first_link(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    # This div contains the article's body
    # (June 2017 Note: Body nested in two div tags)
    content_div = soup.find(id="mw-content-text").find(class_="mw-parser-output")

    # stores the first link found in the article, if the article contains no
    # links this value will remain None
    article_link = None

    # Find all the direct children of content_div that are paragraphs
    for element in content_div.find_all("p", recursive=False):
        # Find the first anchor tag that's a direct child of a paragraph.
        # It's important to only look at direct children, because other types
        # of link, e.g. footnotes and pronunciation, could come before the
        # first link to an article. Those other link types aren't direct
        # children though, they're in divs of various classes.
        if element.find("a", recursive=False):
            article_link = element.find("a", recursive=False).get('href')
            break

    if not article_link:
        return

    # Build a full url from the relative article_link url
    first_link = urllib.parse.urljoin('https://en.wikipedia.org/', article_link)

    return first_link


article_chain = ['https://en.wikipedia.org/wiki/Al-Samoud_2']
target_url = "https://en.wikipedia.org/wiki/Philosophy"

while continue_crawl(article_chain, target_url):
    print(article_chain[-1])
    first_link = find_first_link(article_chain[-1])
    if not first_link:
        print("We've arrived at an article with no links, aborting search!")
        break

    # add the first link to article_chain
    article_chain.append(first_link)
    # delay for about two seconds
    time.sleep(2)

for article in article_chain:
    print(article)
