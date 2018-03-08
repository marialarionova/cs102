import requests
from bs4 import BeautifulSoup

def extract_news(parser):
    """ Extract news from a given web page """

    news_list = []
    for i in range(0, 90, 3):
        news = {'author': parser.table.findAll('table')[1].findAll('tr')[i+1].findAll('td')[1].a.contents[0],
                'title': parser.table.findAll('table')[1].findAll('tr')[i].findAll('td')[2].a.contents[0],
                'comments': parser.table.findAll('table')[1].findAll('tr')[i+1].findAll('td')[1].findAll('a')[5].contents[0],
                'points': parser.table.findAll('table')[1].findAll('tr')[i+1].findAll('td')[1].span.contents[0],
                'url': parser.table.findAll('table')[1].findAll('tr')[i].findAll('td')[2].a['href']}
        news_list.append(news)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.findAll('table')[1].findAll('a')[-1]['href']


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
