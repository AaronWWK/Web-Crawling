from lxml import etree
import requests
import pandas as pd
import re
import time

#
# url = 'https://movie.douban.com/top250?start=225*25&filter='
# header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
#
# res = requests.get(url, headers = header)
# content = etree.HTML(res.text)
# content
# films = content.xpath('//*[@id="content"]/div/div[1]/ol/li')
# films
# film_ch_name = content.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')[0]
# film_ch_name
# film_en_name = content.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[2]/text()')[0]
# film_en_name
# score = content.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')[0]
# score
# brief = content.xpath('//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[2]/span/text()')[0]
# brief


file_info = pd.DataFrame()
for i in range(10):
    url = 'https://movie.douban.com/top250?start={}&filter='
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    res = requests.get(url.format(i*25), headers = header)
    content = etree.HTML(res.text)
    content
    films = content.xpath('//*[@id="content"]/div/div[1]/ol/li')

    for film in films:
        film_ch_name = film.xpath('div/div[2]/div[1]/a/span[1]/text()')[0]  ## there should be no / before div, like xpath('/div/div[2]/div[1]/a/span[1]/text()')[0]
        film_en_name = film.xpath('div/div[2]/div[1]/a/span[2]/text()')[0]
        score = film.xpath('div/div[2]/div[2]/div/span[2]/text()')[0]
        try:
            brief = film.xpath('div/div[2]/div[2]/p[2]/span/text()')[0]
        except:
            brief = None
        temp = pd.DataFrame({'Chinese Name':[film_ch_name],
                             'English Name':[film_en_name],
                             'Score': [score],
                             'Brief': [brief]})
        file_info = pd.concat([file_info, temp])
    time.sleep(1)

file_info.to_csv('Top 250 Movies.csv')

data = pd.read_csv('Top 250 Movies.csv')
data = data.reindex()
data = data.drop(['Unnamed: 0'], axis =1)
data.head()

data.to_csv('Top 250 Movies Reinx.csv')
