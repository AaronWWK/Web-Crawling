from lxml import etree
import requests
import pandas as pd
import re
import time


url = 'https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C%E7%89%87&type=5&interval_id=100:90&action='
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

html = requests.get(url, headers = header)

content = etree.HTML(html.text)
content

movie = content.xpath('//div[@class="moive-list-panel pictext"]')
movie


movie_name = content.xpath('//*[@id="content"]/div/div[1]/div[6]')   #/div[1]/div/div/div[1]/span[1]/a/text()
movie_name
len(movie_name)

print(content.xpath('//div[@class="movie-list-panel pictext"]'))

name = content.xpath('//span[@class="movie-name-text"]/a[1]')

name = content.xpath('//div[class="movie-list-item playable unwatched"]')
name





import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

url = 'https://movie.douban.com/typerank?type_name=%E5%8A%A8%E4%BD%9C%E7%89%87&type=5&interval_id=100:90&action='
html = urllib.request.urlopen(url).read()

soup = BeautifulSoup(html, 'html.parser')
content_list = soup.find(class_="movie-list-panel pictext").find_all(class_="movie-info")

print(content_list)






import urllib.request, urllib.parse, urllib.error
import json
import pandas

result = pd.DataFrame()
for i in range(0,14):
    url = 'https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start={}&limit=20'
    url = urllib.request.urlopen(url.format(i*20))
    data = url.read().decode()

    js = json.loads(data)

    for movie in js:
        name = movie['title']
        region = movie['regions'][0]
        release_date = movie['release_date']
        type = movie['types']
        score = movie['score']
        url = movie['url']
        temp = pd.DataFrame({'Name': [name],
                             'region': [region],
                             'release_date': [release_date],
                             'type': [type],
                             'score': [score],
                             'url': [url]})
        result = pd.concat([result, temp])


result.to_csv('Top 10% Movie.csv')

data = pd.read_csv('Top 10% Movie.csv')
data = data.reindex()
data = data.drop(['Unnamed: 0'], axis =1)
data.head()

data.to_csv('Top 10% Movie.csv')
