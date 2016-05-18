# -*- coding: utf-8 -*-
import sys
from bs4 import BeautifulSoup
import urllib
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


def get_title(soup):
    title = soup.find('div', id="container")\
        .findNext('h2').text.strip().encode('utf-8')
    return title


def get_info(soup, text):
    try:
        info = soup.find('th', text=text)\
            .findNext('td').text.strip().encode('utf-8')
    except:
        info = ''
    return info


if __name__ == '__main__':

    todays_date = str(datetime.now())
    portals = [['open', 'https://www.tenders.gov.au/?startRow=0&event=public%2EATM%2Elist'],
               ['closed', 'https://www.tenders.gov.au/?startRow=0&event=public%2EATM%2Eclosed']]
    errors = []
    country_code = 'au'

    for sp in portals:
        p = sp[1]
        try:
            last_page = get_pages(p)
            for p_num in range(0, last_page):

                try:
                    print p_num
                    page = p[:p.find('Row=')+4] + str(p_num*15) + p[p.find('&event'):]
                    print page
                    links = get_links(page)
                except Exception as e:
                    errors.append([page, e])
                    continue

                for link in links:
                    try:
                        print link
                        tender_soup = get_soup(link)
                        status = sp[0]
                        tender_url = link
                        uuid = link[link.find('UUID=')+5:]
                        title = get_title(tender_soup)
                        amt_id = get_info(tender_soup, 'ATM ID')
                        agency = get_info(tender_soup, 'Agency')
                        category = get_info(tender_soup, 'Category')
                        deadline = get_info(tender_soup, 'Close Date & Time')
                        publish_date = get_info(tender_soup, 'Publish Date')
                        location = get_info(tender_soup, 'Location')
                        multi_agency_access= get_info(tender_soup, 'Multi Agency Access')
                        panel_arrangement = get_info(tender_soup, 'Panel Arrangement')
                        description = get_info(tender_soup, 'Description')
                        other_instructions = get_info(tender_soup, 'Other Instructions ')
                        conditions_for_participation = get_info(tender_soup, 'Conditions for Participation')
                        delivery_timeframe = get_info(tender_soup, 'Timeframe for Delivery')
                        lodgement_address = get_info(tender_soup, 'Address for Lodgement')
                        contact_officer = get_info(tender_soup, 'Contact Officer')
                        phone = get_info(tender_soup, 'Phone Number')
                        email = get_info(tender_soup, 'Email Address')


                        data = {"tender_url":unicode(tender_url),
                                "country_code": unicode(country_code),
                                "status": unicode(status),
                                "uuid": unicode(uuid),
                                "title": unicode(title),
                                "amt_id": unicode(amt_id),
                                "agency": unicode(agency),
                                "category": unicode(category),
                                "deadline": unicode(deadline),
                                "publish_date": unicode(publish_date),
                                "location": unicode(location),
                                "multi_agency_access": unicode(multi_agency_access),
                                "panel_arrangement": unicode(panel_arrangement),
                                "description": unicode(description),
                                "other_instructions": unicode(other_instructions),
                                "conditions_for_participation": unicode(conditions_for_participation),
                                "delivery_timeframe": unicode(delivery_timeframe),
                                "lodgement_address": unicode(lodgement_address),
                                "contact_officer": unicode(contact_officer),
                                "phone": unicode(phone),
                                "email": unicode(email),
                                "date": todays_date}

                        scraperwiki.sqlite.save(unique_keys=['tender_url'], data=data)

                    except Exception as e:
                        errors.append([link, e])
        except KeyboardInterrupt:
            sys.exit("forced exit")

    print 'No. errors ', len(errors)
    print errors

    print 'Addenda Available with login'