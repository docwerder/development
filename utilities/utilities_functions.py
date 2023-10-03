from bs4 import BeautifulSoup
import requests


def scan_func(url: str):
    db = []
    site_tmp = requests.get(url)

    soup_tmp = BeautifulSoup(site_tmp.content, 'html.parser')

    print(f'scanning Site: {url}, Response: {site_tmp}')

    data_site_page = soup_tmp.find_all('a')

    for lf in data_site_page:
        db.append(lf.get('href'))

    #print(f' db of {url}: ', db)
    return db


def indices(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
            #print(offset)
        except ValueError:
            return result
        result.append(offset)

def indices_2(lst, element):
    result = []
    offset = -1
    while True:
        try:
            offset = lst.index(element, offset+1)
            #print(offset)
        except ValueError:
            return result
        result.append(offset)