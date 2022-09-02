import sys
sys.path.append('/Users/joerg/repos/development')
from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd

url = 'http://usenet-4all.pw/'
db = []
titles = []
site_tmp = requests.get(url)

soup_tmp = BeautifulSoup(site_tmp.content, 'html.parser')

print(f'scanning Site: {url}, Response: {site_tmp}')

data_site_page = soup_tmp.find_all('a')

for lf in data_site_page:
    db.append(lf.get('href'))



titles = []
db1 = soup_tmp.find_all("div", {"class": "elementor-text-editor elementor-clearfix"})
#db2 = soup_tmp.find_all({"div class": "elementor-text-editor elementor-clearfix"})
#print(f' db : ', db1)
for lf in db1:
    titles.append(lf.text)