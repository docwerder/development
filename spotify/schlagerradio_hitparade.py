import sys
sys.path.append('/Users/joerg/repos/braz/')
from bs4 import BeautifulSoup
import requests
import pandas as pd
#from utilities_functions import scan_func

def get_top_50():

    url = 'https://www.schlagerradio.de/hitparade'
    db = []
    titles = []
    site_tmp = requests.get(url)

    soup_tmp = BeautifulSoup(site_tmp.content, 'html.parser')

    print(f'scanning Site: {url}, Response: {site_tmp}')

    #soup_tmp.find_all("div", {"class": "stylelistrow"})
    data_site_page = soup_tmp.find_all('a')
b
    for lf in data_site_page:
        db.append(lf.get('href'))

    # print(f' db of {url}: ', db)

    #db = scan_func('https://www.schlagerradio.de/hitparade')
    titles = []
    db1 = soup_tmp.find_all("div", {"class": "totalpoll-question-choices-item-label"})

    for lf in db1:
        titles.append(lf.text)

    titles_db = []

    for title in titles:
        titles_db.append(title)
        #print(title)

    return titles_db
    print(titles_db)

if __name__ == '__main__':
    schlagerradio_hitparade = get_top_50()
    print('schlagerradio_hitparade: ', schlagerradio_hitparade)
    hitparade_db = {'Titel': list(schlagerradio_hitparade)}
    df_hitparade = pd.DataFrame(hitparade_db)

    df_hitparade.to_csv('top_50_schlagerradio_18_07_2022.csv')

