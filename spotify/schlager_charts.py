import sys
sys.path.append('/Users/joerg/repos/development/spotify')
from bs4 import BeautifulSoup
import requests
import itertools
import pandas as pd

url = 'https://schlager-charts.com/single-top-20/'
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


title_str_tmp = titles
#print(title_str_tmp)
node = '\nTOP-PLAYLISTSchlager Charts Top 100 '
titles_string = itertools.dropwhile(lambda x: x != node, title_str_tmp)
#print(it)
next(titles_string)
for single_title in titles_string:
    print(single_title)



#print('list: ', title_str_tmp.'\nTOP-PLAYLISTSchlager Charts Top 100 ')
# <div class="elementor-text-editor elementor-clearfix">
# 				<p><b><span style="color: #000000;">ROLAND KAISER</span><br></b><span style="color: #993300;"><b>Gegen die Liebe kommt man nicht an</b></span></p>					</div>