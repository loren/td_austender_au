# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
from splinter import Browser
import sys
import urllib
import time
from datetime import datetime
import scraperwiki

reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


def get_soup(url):
    html = urllib.urlopen(url)
    soup = BeautifulSoup(html, "lxml")
    return soup


def get_pages(url):
    soup = get_soup(url)
    lp = soup.find('a', text='2')\
        .findPrevious('strong').text
    last_page = int(lp[lp.rfind(' ')+1:])
    print last_page
    return last_page


def get_links(url):
    links = []
    soup = get_soup(url)
    try:
        page_links = soup.findAll('th', text='ATM ID')
        for l in page_links:
            links.append(url[:27] + l.findNext('a')['href'])
    except:
        links = []
    return links


if __name__ == '__main__':

    todays_date = str(datetime.now())
    portals = ['https://www.tenders.gov.au/?startRow=0&event=public%2EATM%2Elist',
               'https://www.tenders.gov.au/?startRow=0&event=public%2EATM%2Eclosed']

    for p in portals:

        last_page = get_pages(p)
        for p_num in range(0, last_page):


            page = p[:p.find('Row=')+4] + str(p_num*15) + p[p.find('&event'):]
            print page
            links = get_links(page)
            for link in links:
                print link




