from lxml import etree
import pandas as pd
import requests
import time
import re



result = pd.DataFrame()
for i in range(0,250,25):
    header ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url ='https://book.douban.com/top250?start={}'

    html = requests.get(url.format(i), headers = header)  # headers  not headers
    bs = etree.HTML(html.text)

    for item in bs.xpath('//tr[@class="item"]'):
        #Book name
        book_name = item.xpath('td[2]/div[1]/a[1]/@title')[0]  # 直接获取属性值
        #Book Info
        book_info = item.xpath('td[2]/p[@class="pl"]')[0].text # 匹配属性值为@class="pl" 的节点
        #Rating amount
        rating_amount = re.findall('\d+\S+' ,item.xpath('td[2]/div[2]/span[3]')[0].text)[0]
        #Rating
        rating = item.xpath('td[2]/div[2]/span[2]')[0].text
        #Brief
        try:
            brief = item.xpath('td[2]/p[@class="quote"]/span')[0].text
        except:
            brief = None

        # temp save the result for every page
        temp = pd.DataFrame({'Book Name': [book_name],
                             'Book Info': [book_info],
                             'Rating Amount': [rating_amount],
                             'Score': [rating],
                             'Brief': [brief]})
        result = pd.concat([result, temp])
    time.sleep(5)

result.to_csv('Douban2.csv')

data = pd.read_csv('Douban2.csv')
data.reindex()
data = data.drop(['Unnamed: 0'], axis=1)
data.sort_values('Score', inplace = True, ascending = False)
data
data.to_csv('Douban2.csv')
